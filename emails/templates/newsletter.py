NEWSLETTER_OUTLINE = """
<div style="margin:0;padding:0;background-color:#fff">
  <table style="table-layout:fixed;vertical-align:top;min-width:320px;border-spacing:0;border-collapse:collapse;background-color:#fff;width:100%" cellpadding="0" cellspacing="0" role="presentation" width="100%" bgcolor="#fff" valign="top">
      <tbody>
          <tr style="vertical-align:top" valign="top">
              <td style="word-break:break-word;vertical-align:top" valign="top">
                  {SECTION_BODY}
              </td>
          </tr>
      </tbody>
  </table>
</div>

"""

GROUP_PICTURE_HEADER = """
    <div style="background-color:transparent">
        <div class="m_-8684494649613928784block-grid" style="Margin:0 auto;min-width:320px;max-width:500px;word-wrap:break-word;word-break:break-word;background-color:transparent">
            <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
                <div class="m_-8684494649613928784col" style="min-width:320px;max-width:500px;display:table-cell;vertical-align:top;width:500px">
                    <div style="width:100%!important">             
                        <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:40px;padding-bottom:15px;padding-right:0px;padding-left:0px"> 
                            <div align="center" style="padding-right:0px;padding-left:0px">
                                <img align="center" border="0" src={PROFILE_PICTURE_URL} style="text-decoration:none;height:auto;border:0;width:100%;max-width:45px;display:block;border-radius:50%" width="45">            
                            </div>     
                        </div> 
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

GROUP_NAME_ISSUE_HEADER = """
<div style="background-color:transparent">
    <div class="m_3017872216071107836block-grid" style="min-width:320px;max-width:500px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:#ffffff">
        <div style="border-collapse:collapse;display:table;width:100%;background-color:#ffffff">
            <div class="m_3017872216071107836col" style="min-width:320px;max-width:500px;display:table-cell;vertical-align:top;width:500px">
                <div class="m_3017872216071107836col_cont" style="width:100%!important">
                    <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:25px;padding-bottom:0px;padding-right:0px;padding-left:0px">
                        <div style="color:#000000;font-family:'Source Serif Pro',Georgia,Times,serif;line-height:1.2;padding-top:5px;padding-right:0px;padding-bottom:5px;padding-left:0px">
                            <!-- TODO REPLACE GROUP NAME HERE -->
                            <div style="line-height:1.2;font-size:12px;font-family:'Source Serif Pro',Georgia,Times,serif;color:#000000">
                                <p style="margin:0;font-size:34px;line-height:1.2;word-break:break-word;text-align:center;font-family:'Source Serif Pro',Georgia,Times,serif;margin-top:0;margin-bottom:0"><span style="color:#000000;font-size:34px"><strong>{GROUP_NAME}</strong></span></p>
                            </div>
                        </div>
                        <!-- TODO REPLACE GROUP ISSUE AND DATE HERE  -->
                        <div style="color:#000000;font-family:'Source Serif Pro',Georgia,Times,serif;line-height:1.2;padding-top:5px;padding-right:0px;padding-bottom:5px;padding-left:0px">
                            <div style="line-height:1.2;font-size:12px;font-family:'Source Serif Pro',Georgia,Times,serif;color:#000000">
                                <p style="margin:0;font-size:16px;line-height:1.2;word-break:break-word;text-align:center;font-family:'Source Serif Pro',Georgia,Times,serif;margin-top:0;margin-bottom:0"><span style="color:#000000;font-size:16px"><strong><span>Issue No.{ISSUE_NUMBER} · {ISSUE_DATE}</span></strong></span></p>
                            </div>
                        </div>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;min-width:100%" role="presentation" valign="top">
                            <tbody>
                                <tr style="vertical-align:top" valign="top">
                                    <td style="word-break:break-word;vertical-align:top;min-width:100%;padding-top:10px;padding-right:0px;padding-bottom:0px;padding-left:0px" valign="top">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;border-top:1px solid #626262;width:100%" align="center" role="presentation" valign="top">
                                            <tbody>
                                                <tr style="vertical-align:top" valign="top">
                                                    <td style="word-break:break-word;vertical-align:top;height:0;line-height:0" valign="top"><span></span></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

SECTION_HEADER = """
<div style="background-color:transparent">
    <div class="m_3017872216071107836block-grid" style="min-width:320px;max-width:500px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:transparent">
        <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
            <div class="m_3017872216071107836col" style="min-width:320px;max-width:500px;display:table-cell;vertical-align:top;width:500px">
                <div class="m_3017872216071107836col_cont" style="width:100%!important">
                    <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:35px;padding-bottom:20px;padding-right:0px;padding-left:0px">
                        <div style="color:#555555;font-family:'Source Serif Pro',Georgia,Times,serif;letter-spacing:0px;line-height:1.5;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px">
                            <div style="font-size:12px;line-height:1.5;font-family:'Source Serif Pro',Georgia,Times,serif;color:#555555;letter-spacing:0px">
                                <p style="margin:0;font-size:18px;line-height:1.5;word-break:break-word;text-align:left;font-family:'Source Serif Pro',Georgia,Times,serif;letter-spacing:normal;margin-top:0;margin-bottom:0"><span style="font-size:18px"><strong style="color:#000000">{SECTION_NAME}</strong></span></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

SECTION_BODY = """
<div style="background-color:transparent">
    <div class="m_3017872216071107836block-grid" style="min-width:320px;max-width:500px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:#faf5f1">
        <div style="border-collapse:collapse;display:table;width:100%;background-color:#faf5f1">
            <div class="m_3017872216071107836col" style="min-width:320px;max-width:500px;display:table-cell;vertical-align:top;width:500px">
                <div class="m_3017872216071107836col_cont" style="width:100%!important">
                    <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:0px;padding-bottom:15px;padding-right:0px;padding-left:0px">
                        <!-- TODO EXAMPLE QUESTION AND ANSWER TEMPLATE  -->
                        {SECTION_QUESTION}
                        {SECTION_ANSWERS}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

SECTION_QUESTION = """
<div style="background-color:transparent">
                      <div class="m_3017872216071107836block-grid" style="min-width:320px;max-width:500px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:#faf5f1">
                          <div style="border-collapse:collapse;display:table;width:100%;background-color:#faf5f1">
                              
                              
                              <div class="m_3017872216071107836col" style="min-width:320px;max-width:500px;display:table-cell;vertical-align:top;width:500px">
                                  <div class="m_3017872216071107836col_cont" style="width:100%!important">
                                      
                                      <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:15px;padding-bottom:5px;padding-right:0px;padding-left:0px">
                                          
                                          
                                          <div style="color:#555555;font-family:DM Sans,Arial,sans-serif;line-height:1.5;padding-top:10px;padding-right:25px;padding-bottom:0px;padding-left:25px">
                                              <div style="line-height:1.5;font-size:12px;font-family:DM Sans,Arial,sans-serif;color:#555555">
                                                  <p style="margin:0;font-size:15px;line-height:1.5;word-break:break-word;font-family:DM Sans,Arial,sans-serif;margin-top:0;margin-bottom:0"><span style="color:#000000;font-size:15px"><span><span><span><span><em><em>{AUTHOR} asked:</em> {QUESTION}</em></span></span></span></span></span></p>
                                              </div>
                                          </div>
                                          
                                          <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;min-width:100%" role="presentation" valign="top">
                                              <tbody>
                                                  <tr style="vertical-align:top" valign="top">
                                                      <td style="word-break:break-word;vertical-align:top;min-width:100%;padding-top:10px;padding-right:20px;padding-bottom:15px;padding-left:20px" valign="top">
                                                          <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;border-top:1px solid #e1dad4;width:100%" align="center" role="presentation" valign="top">
                                                              <tbody>
                                                                  <tr style="vertical-align:top" valign="top">
                                                                      <td style="word-break:break-word;vertical-align:top;height:0;line-height:0" valign="top"><span></span></td>
                                                                  </tr>
                                                              </tbody>
                                                          </table>
                                                      </td>
                                                  </tr>
                                              </tbody>
                                          </table>
                                          
                                      </div>
                                      
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
"""

SECTION_ANSWER = """
<div style="color:#000000;font-family:DM Sans,Arial,sans-serif;line-height:1.5;padding-top:5px;padding-right:25px;padding-bottom:10px;padding-left:25px">
    <div style="line-height:1.5;font-size:12px;font-family:DM Sans,Arial,sans-serif;color:#000000">
        <p style="margin:0;font-size:15px;line-height:1.5;word-break:break-word;text-align:left;font-family:DM Sans,Arial,sans-serif;margin-top:0;margin-bottom:0"><span style="color:#000000;font-size:15px"><span><span style="color:#133f63"><strong>{NAME}</strong></span>: <span>{ANSWER}</span></span></span></p>
    </div>
</div>
"""

SECTION_SPACE_BETWEEN = """
<div style="background-color:transparent">
    <div class="m_3017872216071107836block-grid" style="min-width:320px;max-width:500px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:transparent">
        <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
            <div class="m_3017872216071107836col" style="min-width:320px;max-width:500px;display:table-cell;vertical-align:top;width:500px">
                <div class="m_3017872216071107836col_cont" style="width:100%!important">
                    <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:0px;padding-bottom:0px;padding-right:0px;padding-left:0px">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;min-width:100%" role="presentation" valign="top">
                            <tbody>
                                <tr style="vertical-align:top" valign="top">
                                    <td style="word-break:break-word;vertical-align:top;min-width:100%;padding-top:5px;padding-right:5px;padding-bottom:5px;padding-left:5px" valign="top">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;border-top:7px solid #ffffff;width:100%" align="center" role="presentation" valign="top">
                                            <tbody>
                                                <tr style="vertical-align:top" valign="top">
                                                    <td style="word-break:break-word;vertical-align:top;height:0;line-height:0" valign="top"><span></span></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table> 
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

MADE_BY = """
<div style="color:#000000;font-family:DM Sans,Arial,sans-serif;line-height:1.5;padding-top:5px;padding-right:25px;padding-bottom:5px;padding-left:25px">
    <div style="font-size:12px;line-height:1.5;color:#000000;font-family:DM Sans,Arial,sans-serif">
        <p style="margin:0;font-size:15px;text-align:center;line-height:1.5;word-break:break-word;margin-top:0;margin-bottom:0"><span style="font-size:15px">🖋 Made by {MEMBER_NAMES}</span></p>
    </div>
</div>
"""

NEXT_ISSUE_DATE = """
<div style="color:#555555;font-family:DM Sans,Arial,sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px">
    <div style="line-height:1.2;font-size:12px;font-family:DM Sans,Arial,sans-serif;color:#555555">
        <p style="margin:0;font-size:15px;line-height:1.2;word-break:break-word;text-align:center;font-family:DM Sans,Arial,sans-serif;margin-top:0;margin-bottom:0"><span style="font-size:15px"><span style="color:#000000">Your next issue will be delivered on:</span></span></p>
        <p style="margin:0;font-size:15px;line-height:1.2;word-break:break-word;text-align:center;font-family:DM Sans,Arial,sans-serif;margin-top:0;margin-bottom:0">&nbsp;</p>
        <p style="margin:0;font-size:15px;line-height:1.2;word-break:break-word;text-align:center;font-family:DM Sans,Arial,sans-serif;margin-top:0;margin-bottom:0"><span style="color:#000000;font-size:15px"><strong><span>{NEXT_ISSUE_DATE}</span></strong></span></p>
    </div>
</div>
"""

ENDING = """
<div style="background-color:transparent">
    <div class="m_3017872216071107836block-grid" style="min-width:320px;max-width:500px;word-wrap:break-word;word-break:break-word;Margin:0 auto;background-color:transparent">
        <div style="border-collapse:collapse;display:table;width:100%;background-color:transparent">
            <div class="m_3017872216071107836col" style="min-width:320px;max-width:500px;display:table-cell;vertical-align:top;width:500px">
                <div class="m_3017872216071107836col_cont" style="width:100%!important">
                    <div style="border-top:0px solid transparent;border-left:0px solid transparent;border-bottom:0px solid transparent;border-right:0px solid transparent;padding-top:40px;padding-bottom:0px;padding-right:0px;padding-left:0px">
                        {MADE_BY}
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;min-width:100%" role="presentation" valign="top">
                            <tbody>
                                <tr style="vertical-align:top" valign="top">
                                    <td style="word-break:break-word;vertical-align:top;min-width:100%;padding-top:40px;padding-right:0px;padding-bottom:40px;padding-left:0px" valign="top">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;vertical-align:top;border-spacing:0;border-collapse:collapse;border-top:2px solid #eaeaea;width:100%" align="center" role="presentation" valign="top">
                                            <tbody>
                                                <tr style="vertical-align:top" valign="top">
                                                    <td style="word-break:break-word;vertical-align:top;height:0;line-height:0" valign="top"><span></span></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        {NEXT_ISSUE_DATE}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""
