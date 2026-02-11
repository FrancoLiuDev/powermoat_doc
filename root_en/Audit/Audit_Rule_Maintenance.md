# Audit Rule維護

**Notification Level Setting and Audit Ruledesign**

  #@img_AD0005/image123.png

**Notification Level Setting: Set various notification levels**

**Add Notification Level (Notification Category: Immediate, Batch, Log Only)**

  #@img_AD0005/image124.png

**Notification Level Setting：修改。點擊[Edit Icon] 即可EnterEdit修改**

  #@img_AD0005/image125.png

**\
**

**Notification Level Setting：刪除。點擊[Delete Icon] 即可刪除。**

  #@img_AD0005/image126.png

**Audit Ruledesign：Combine rules based on keyword settings to formulate notification levels**

  #@img_AD0005/image127.png

**Audit Ruledesign：可perform新增、修改、刪除。**

  #@img_AD0005/image128.png

Condition: Set detection conditions as needed (ex: General Keyword (score) >= 1)

Notification Level: Which notification level to execute when the above conditions are met.

Multiple Condition Rule Setting Example

  #@img_AD0005/image129.png

When document content has "Confidential" AND (文件Content  contains  "designDiagram" OR "Circuit") the condition is met, triggering a notification event。
