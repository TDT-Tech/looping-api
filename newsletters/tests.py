# Create your tests here.
from django.forms.models import model_to_dict
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from newsletters.models import Answer, Newsletter
from newsletters.serializers import NewsletterCreateSerializer, NewsletterSerializer
from utils.tests.factory import (
    AnswerFactory,
    GroupMemberFactory,
    NewsletterFactory,
    QuestionFactory,
    UserFactory,
    UserWithGroupFactory,
)


class NewsletterSerializerTests(TestCase):
    def setUp(self):
        self.user = UserWithGroupFactory()
        self.group = self.user.group_set.first()
        self.question = QuestionFactory(group=self.group)
        self.second_question = QuestionFactory(group=self.group)

    def test_create_succeeds(self):
        serializer_data = {
            "group": self.group.id,
            "questions": [self.question.id],
            "status": Newsletter.Status.INPROGRESS,
        }
        serializer = NewsletterCreateSerializer(data=serializer_data)
        serializer.is_valid()
        new_newsletter = serializer.save()
        new_newsletter.refresh_from_db()

        self.assertEqual(new_newsletter.questions.first(), self.question)
        self.assertIsNotNone(new_newsletter.issue_date)

    def test_update_succeeds(self):
        newsletter = NewsletterFactory(questions=[self.question], group=self.group)
        self.assertEqual(newsletter.questions.first(), self.question)

        updated_data = {
            "group": self.group.id,
            "questions": [],
            "status": Newsletter.Status.INPROGRESS,
        }
        updated_serializer = NewsletterSerializer(newsletter, data=updated_data)
        updated_serializer.is_valid()
        updated_newsletter = updated_serializer.save()

        self.assertFalse(updated_newsletter.questions.exists())

    def test_update_fails_if_newsletter_status_not_upcoming_or_inprogress(self):
        newsletter = NewsletterFactory(questions=[self.question], group=self.group)
        self.assertEqual(newsletter.questions.first(), self.question)

        updated_data = {
            "group": self.group.id,
            "questions": [],
            "status": Newsletter.Status.DELIVERED,
        }
        updated_serializer = NewsletterSerializer(newsletter, data=updated_data)
        updated_serializer.is_valid()
        updated_newsletter = updated_serializer.save()
        self.assertTrue(updated_newsletter.questions.exists())

    def test_removing_question_from_newsletter_deletes_answer(self):
        newsletter = NewsletterFactory(
            questions=[self.question, self.second_question], group=self.group
        )
        AnswerFactory(
            question=self.question, newsletter=newsletter, submitter=self.user
        )
        AnswerFactory(
            question=self.second_question, newsletter=newsletter, submitter=self.user
        )
        self.assertTrue(
            Answer.objects.filter(
                question_id=self.question.id, newsletter=newsletter
            ).exists()
        )

        updated_data = {
            "group": self.group.id,
            "questions": [model_to_dict(self.second_question)],
            "status": Newsletter.Status.INPROGRESS,
        }
        updated_serializer = NewsletterSerializer(newsletter, data=updated_data)
        updated_serializer.is_valid()
        updated_serializer.save()

        self.assertFalse(
            Answer.objects.filter(
                question_id=self.question.id, newsletter=newsletter
            ).exists()
        )
        self.assertTrue(
            Answer.objects.filter(
                question_id=self.second_question.id, newsletter=newsletter
            ).exists()
        )


class AnswerViewSetTests(APITestCase):
    def setUp(self):
        self.user = UserWithGroupFactory()
        self.group = self.user.group_set.first()
        self.newsletter = NewsletterFactory(
            group=self.group, questions=[QuestionFactory(group=self.group)]
        )
        self.answer = AnswerFactory(
            question=self.newsletter.questions.first(),
            newsletter=self.newsletter,
            submitter=self.user,
        )
        self.answer_url = f"/newsletters/{self.newsletter.id}/answers/"
        self.client.force_authenticate(user=self.user)

    def test_retrieve_newsletter_answers_returns_users_answers(self):
        AnswerFactory(
            question=self.newsletter.questions.first(),
            newsletter=self.newsletter,
            submitter=UserFactory(email="test@test.com", name="Test"),
        )
        response = self.client.get(self.answer_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(1, len(data))
        self.assertEqual(data[0]["id"], self.answer.id)
        self.assertEqual(data[0]["answer"], self.answer.answer)
        self.assertEqual(data[0]["submitter"], self.user.id)

    def test_retrieve_newsletter_answers_does_not_return_other_newsletter_answers(self):
        newsletter = NewsletterFactory(
            group=self.group, questions=[QuestionFactory(group=self.group)]
        )
        new_answer = AnswerFactory(
            question=newsletter.questions.first(),
            newsletter=newsletter,
            submitter=UserFactory(email="test@test.com"),
        )
        response = self.client.get(self.answer_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data[0]["id"], new_answer.id)

    def test_retrieve_newsletter_answer_fails_if_newsletter_does_not_exist(self):
        response = self.client.get("/newsletters/2323232/answers/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_newsletter_answer_fails_if_newsletter_does_not_exist(self):
        answer_payload = [
            {
                "question_id": self.newsletter.questions.first().id,
                "answer": "Test answer",
            }
        ]
        response = self.client.post(
            "/newsletters/12/answers/batch/", data=answer_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_newsletter_answer_fails_if_newsletter_not_in_progress(self):
        answer_payload = [
            {
                "question_id": self.newsletter.questions.first().id,
                "answer": "Test answer",
            }
        ]
        self.newsletter.status = Newsletter.Status.DELIVERED
        self.newsletter.save()
        response = self.client.post(
            f"{self.answer_url}batch/", data=answer_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_newsletter_answer(self):
        answer_payload = [
            {
                "question_id": self.newsletter.questions.first().id,
                "answer": "Test answer",
            }
        ]
        response = self.client.post(
            f"{self.answer_url}batch/", data=answer_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.newsletter.answer_set.count(), 2)
        added_answer = self.newsletter.answer_set.filter(
            answer=answer_payload[0]["answer"]
        )
        self.assertIsNotNone(added_answer)

    def test_add_newsletter_answers(self):
        answer_payload = [
            {
                "question_id": self.newsletter.questions.first().id,
                "answer": "Test answer",
            },
            {
                "question_id": self.newsletter.questions.first().id,
                "answer": "Test answer2",
            },
        ]
        response = self.client.post(
            f"{self.answer_url}batch/", data=answer_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.newsletter.answer_set.count(), 3)
        for answer in answer_payload:
            added_answer = self.newsletter.answer_set.get(answer=answer["answer"])
            self.assertIsNotNone(added_answer)

    def test_add_newsletter_answer_fails_when_not_passed_list(self):
        answer_payload = {
            "question_id": self.newsletter.questions.first().id,
            "answer": "Test answer",
        }
        response = self.client.post(
            f"{self.answer_url}batch/", data=answer_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_newsletter_answer_fails_when_question_does_not_exist(self):
        answer_payload = [{"question_id": 25252, "answer": "Test answer"}]

        self.client.post(f"{self.answer_url}batch/", data=answer_payload, format="json")
        with self.assertRaises(Answer.DoesNotExist):
            self.newsletter.answer_set.get(question_id=answer_payload[0]["question_id"])

    def test_add_newsletter_answer_fails_with_question_not_in_newsletter(self):
        newsletter = NewsletterFactory(
            group=self.group, questions=[QuestionFactory(group=self.group)]
        )
        question = newsletter.questions.first()
        answer_payload = [
            {
                "question_id": question.id,
                "answer": "Test answer",
            }
        ]
        response = self.client.post(
            f"{self.answer_url}batch/", data=answer_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.assertRaises(Answer.DoesNotExist):
            self.newsletter.answer_set.get(question_id=question.id)

    def test_update_newsletter_answer(self):
        answer_payload = [
            {
                "id": self.answer.id,
                "submitter": self.user.id,
                "question": model_to_dict(self.answer.question),
                "answer": "Updated answer",
            }
        ]
        response = self.client.put(
            f"{self.answer_url}batch/", data=answer_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_answer = self.newsletter.answer_set.get(id=self.answer.id)
        self.assertEqual(updated_answer.answer, answer_payload[0]["answer"])

    def test_update_newsletter_answers(self):
        new_answers = [
            AnswerFactory(
                question=self.newsletter.questions.first(),
                newsletter=self.newsletter,
                submitter=self.user,
            )
            for _ in range(2)
        ]
        answer_payload = [
            {
                "id": a.id,
                "submitter": self.user.id,
                "question": model_to_dict(a.question),
                "answer": "Updated answer",
            }
            for a in new_answers
        ]
        response = self.client.put(
            f"{self.answer_url}batch/", data=answer_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i, answer in enumerate(new_answers):
            updated_answer = self.newsletter.answer_set.get(id=answer.id)
            self.assertIsNotNone(updated_answer)
            self.assertEqual(updated_answer.answer, answer_payload[i]["answer"])


class NewsletterAdminAllButMemberReadOnlyPermissionsTests(APITestCase):
    def setUp(self):
        self.user = UserWithGroupFactory()
        self.group = self.user.group_set.first()
        self.newsletter = NewsletterFactory(
            group=self.group, questions=[QuestionFactory(group=self.group)]
        )
        self.user_with_no_group = UserFactory(email="test@test.com")
        self.newsletter_url = f"/newsletters/{self.newsletter.id}/"
        self.update_payload = {"status": Newsletter.Status.UPCOMING}

    def test_user_cannot_access_newsletter_without_membership(self):
        self.client.force_authenticate(user=self.user_with_no_group)
        response = self.client.get(self.newsletter_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_access_newsletter_with_membership(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.newsletter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_member_cannot_update_newsletter(self):
        GroupMemberFactory(
            user=self.user_with_no_group, group=self.user.group_set.first()
        )
        self.client.force_authenticate(user=self.user_with_no_group)
        response = self.client.patch(self.newsletter_url, data=self.update_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_member_cannot_delete_newsletter(self):
        GroupMemberFactory(
            user=self.user_with_no_group, group=self.user.group_set.first()
        )
        self.client.force_authenticate(user=self.user_with_no_group)
        response = self.client.delete(self.newsletter_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_admin_can_update_newsletter(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.newsletter_url, data=self.update_payload)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["status"], self.update_payload["status"])

    def test_group_admin_can_delete_newsletter(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.newsletter_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(self.group.newsletter_set.first())


class IsGroupMemberPermissionTests(APITestCase):
    def setUp(self):
        self.user = UserWithGroupFactory()
        self.user_without_group = UserFactory(email="test@test.com")
        self.group = self.user.group_set.first()
        self.newsletter = NewsletterFactory(
            group=self.group, questions=[QuestionFactory(group=self.group)]
        )
        self.answer = AnswerFactory(
            question=self.newsletter.questions.first(),
            newsletter=self.newsletter,
            submitter=self.user,
        )
        self.answer_payload = {
            "question_id": self.newsletter.questions.first().id,
            "answer": "Test answer",
        }
        self.answer_url = f"/newsletters/{self.newsletter.id}/answers/"
        self.client.force_authenticate(user=self.user)

    def test_non_member_cannot_access_answers(self):
        self.client.force_authenticate(user=self.user_without_group)
        response = self.client.get(self.answer_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_can_access_answers(self):
        response = self.client.get(self.answer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_can_add_answers(self):
        response = self.client.post(
            f"{self.answer_url}batch/", data=[self.answer_payload], format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_member_cannot_add_answers(self):
        self.client.force_authenticate(user=self.user_without_group)
        response = self.client.post(
            f"{self.answer_url}batch/", data=self.answer_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
