REPLY_OUTLINE = """
<div style="margin: 0; padding: 0; background-color: #ffffff;">
  <table
      style="table-layout: fixed; vertical-align: top; min-width: 320px; margin: 0 auto; border-spacing: 0; border-collapse: collapse; background-color: #ffffff; width: 100%;"
      cellpadding="0"
      cellspacing="0"
      role="presentation"
      width="100%"
      bgcolor="#ffffff"
      valign="top"
  >
      <tbody>
          <tr style="vertical-align: top;" valign="top">
              <td style="word-break: break-word; vertical-align: top;" valign="top">
                  <div style="background-color: transparent;">
                      <div class="m_-4793849440357726351block-grid" style="margin: 0 auto; min-width: 320px; max-width: 500px; word-wrap: break-word; word-break: break-word; background-color: transparent;">
                          <div style="border-collapse: collapse; display: table; width: 100%; background-color: transparent;">
                              <div class="m_-4793849440357726351col" style="min-width: 320px; max-width: 500px; display: table-cell; vertical-align: top; width: 500px;">
                                  <div style="width: 100% !important;">
                                      <div
                                          style="
                                              border-top: 0px solid transparent;
                                              border-left: 0px solid transparent;
                                              border-bottom: 0px solid transparent;
                                              border-right: 0px solid transparent;
                                              padding-top: 40px;
                                              padding-bottom: 15px;
                                              padding-right: 0px;
                                              padding-left: 0px;
                                          "
                                      >
                                          <!-- TODO LOGO  -->
                                          {LOGO_SECTION}
                                      </div>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
                  <!-- TODO TEXT USER NAME AND ISSUE -->
                  {REPLY_INTRO_SECTION}
                  {REPLY_BUTTON_SECTION}
                  <!-- THIS WEEKS QUESTION SECTION  -->
                  <div style="background-color: transparent;">
                      <div class="m_-4793849440357726351block-grid" style="margin: 0 auto; min-width: 320px; max-width: 500px; word-wrap: break-word; word-break: break-word; background-color: #f6f4f1;">
                          <div style="border-collapse: collapse; display: table; width: 100%; background-color: #f6f4f1;">
                              <div class="m_-4793849440357726351col" style="min-width: 320px; max-width: 500px; display: table-cell; vertical-align: top; width: 500px;">
                                  <div style="width: 100% !important;">
                                      <div
                                          style="
                                              border-top: 0px solid transparent;
                                              border-left: 0px solid transparent;
                                              border-bottom: 0px solid transparent;
                                              border-right: 0px solid transparent;
                                              padding-top: 5px;
                                              padding-bottom: 5px;
                                              padding-right: 0px;
                                              padding-left: 0px;
                                          "
                                      >
                                          <div style="color: #555555; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 1.8; padding-top: 30px; padding-right: 35px; padding-bottom: 10px; padding-left: 35px;">
                                              <div style="line-height: 1.8; font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; color: #555555;">
                                                  <p style="line-height: 1.8; word-break: break-word; text-align: left; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; font-size: 17px; margin: 0;">
                                                      <span style="color: #000000; font-size: 17px;">
                                                          <strong><span>This week's questions:</span></strong>
                                                      </span>
                                                  </p>
                                              </div>
                                          </div>
                                          {QUESTION_SECTION}
                                      </div>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
              </td>
          </tr>
      </tbody>
  </table>
 </div>
"""

LOGO_SECTION = """
 <div align="center" style="padding-right: 0px; padding-left: 0px;">
    <a
        href={WEBSITE_URL}
        style="outline: none;"
        target="_blank"
    >
        <img
            align="center"
            border="0"
            src={LOGO_URL}
            style="text-decoration: none; height: auto; border: 0; width: 100%; max-width: 45px; display: block; border-radius: 50%;"
            width="45"
        />
    </a>
</div>
"""

REPLY_INTRO_SECTION = """
<div style="background-color: transparent;">
    <div class="m_-4793849440357726351block-grid" style="margin: 0 auto; min-width: 320px; max-width: 500px; word-wrap: break-word; word-break: break-word; background-color: transparent;">
        <div style="border-collapse: collapse; display: table; width: 100%; background-color: transparent;">
            <div class="m_-4793849440357726351col" style="min-width: 320px; max-width: 500px; display: table-cell; vertical-align: top; width: 500px;">
                <div style="width: 100% !important;">
                    <div
                        style="
                            border-top: 0px solid transparent;
                            border-left: 0px solid transparent;
                            border-bottom: 0px solid transparent;
                            border-right: 0px solid transparent;
                            padding-top: 15px;
                            padding-bottom: 0px;
                            padding-right: 0px;
                            padding-left: 0px;
                        "
                    >
                        <div style="color: #555555; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 1.8; padding-top: 10px; padding-right: 0px; padding-bottom: 10px; padding-left: 0px;">
                            <div style="line-height: 1.8; font-size: 12px; color: #555555; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
                                <p style="font-size: 22px; line-height: 1.8; word-break: break-word; text-align: center; margin: 0;">
                                    <span style="font-size: 22px; color: #000000;">
                                        <strong><span style="color: #000000;">Hi {NAME}</span>,&nbsp;</strong>Issue No.{ISSUE_NUMBER} of {NEWSLETTER_NAME} is ready for your reply!
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

REPLY_BUTTON_SECTION = """
<!-- TODO BUTTON TO REPLY AND REDIRECT  -->
<div style="background-color: transparent;">
    <div class="m_-4793849440357726351block-grid" style="margin: 0 auto; min-width: 320px; max-width: 500px; word-wrap: break-word; word-break: break-word; background-color: transparent;">
        <div style="border-collapse: collapse; display: table; width: 100%; background-color: transparent;">
            <div class="m_-4793849440357726351col" style="min-width: 320px; max-width: 500px; display: table-cell; vertical-align: top; width: 500px;">
                <div style="width: 100% !important;">
                    <div
                        style="
                            border-top: 0px solid transparent;
                            border-left: 0px solid transparent;
                            border-bottom: 0px solid transparent;
                            border-right: 0px solid transparent;
                            padding-top: 10px;
                            padding-bottom: 10px;
                            padding-right: 0px;
                            padding-left: 0px;
                        "
                    >
                        <div align="center" style="padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;">
                            <a
                                href="{REPLY_URL}"
                                style="
                                    text-decoration: none;
                                    display: inline-block;
                                    color: #ffffff;
                                    background-color: #56a778;
                                    border-radius: 4px;
                                    width: auto;
                                    width: auto;
                                    border-top: 1px solid #56a778;
                                    border-right: 1px solid #56a778;
                                    border-bottom: 1px solid #56a778;
                                    border-left: 1px solid #56a778;
                                    padding-top: 10px;
                                    padding-bottom: 10px;
                                    font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
                                    text-align: center;
                                    word-break: keep-all;
                                "
                                target="_blank"
                            >
                                <span style="padding-left: 25px; padding-right: 25px; font-size: 16px; display: inline-block;">
                                    <span style="font-size: 16px; line-height: 2; word-break: break-word;"><strong>Add Your Reply&nbsp; ➝</strong></span>
                                </span>
                            </a>
                        </div>
                        <!-- TODO UPDATE TO NEWSLETTER ISUE DATE -->
                        <div style="color: #555555; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 1.8; padding-top: 30px; padding-right: 10px; padding-bottom: 30px; padding-left: 10px;">
                            <div style="line-height: 1.8; font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; color: #555555;">
                                <p style="font-size: 15px; line-height: 1.8; word-break: break-word; text-align: center; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; margin: 0;">
                                    <span style="font-size: 15px; color: #000000;">Reply by {ISSUE_DATE}</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

QUESTION_SECTION = """
<!-- QUESTION SECTION BUILD TODO -->
<div style="color: #555555; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 1.8; padding-top: 0px; padding-right: 25px; padding-bottom: 25px; padding-left: 25px;">
    <div style="line-height: 1.8; font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; color: #555555;">
        <ul>
            {QUESTION_ITEMS}
        </ul>
    </div>
</div>
"""

QUESTION_SECTION_ITEM = """
<li style="text-align: left; line-height: 1.8;">
    <span style="color: #2d2c2c;"><span style="font-size: 16px;">{QUESTION}</span></span><span style="color: #2d2c2c;"></span>
</li>
"""
