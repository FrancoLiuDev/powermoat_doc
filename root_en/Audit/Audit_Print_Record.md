# Audit_Print_Record

  #@img_AD0003/image134.png

- Query Conditions:

  - Print Start Date and End Date: Specify query date range

  - User Account: Specify records of a user

  - Department：Specify records of a department

  - Device Name: Specify records of a device

  - Execution Status: Specify print job execution status (Default: Print Completed)

  - Remark：SpecifyRemark的text

  - Risk Index: Risk index must exceed this score

  - Keyword Full-text Search: Document OCR content contains specified keywords

**\
**

**Filter Condition Save**

  #@img_AD0003/image135.png

If query condition name is the same, overwrite old condition.

**Filter Condition Load**

  #@img_AD0003/image136.png

After selecting condition item, apply to load filter condition or apply and execute.

**\
**

Audit Retrieval Print Detailed Record

  #@img_AD0003/image137.png

- Risk Info: Display total risk index of this document

- Print Info: Display relevant info of this document

- Right side is image and OCR content display block

  - Search box above can input search string; if matched, it will match before page number "\*"

  - Risk info block displays results matching keyword comparison

  - OCR辨識Content顯示此Image的textContent，if keywords match, they will be highlighted

  - Image thumbnail can be clicked to display large image view.

  #@img_AD0003/image138.png

View Image Security Mode (PINCODE)

  #@img_AD0003/image139.png

若啟用時，調閱Image時需要輸入 PIN CODE(系統會寄送至Email信箱)後才能performImage檢視。

View Image Security Mode (Dual Authentication)

  #@img_AD0003/image140.png

When dual authentication mode is enabled, a second auditor must be assigned for each auditor.

Second auditor can be specified application roles (multiple) or specified accounts (multiple)

  #@img_AD0003/image141.png

When viewing image, must log in as specified second auditor to view image.
