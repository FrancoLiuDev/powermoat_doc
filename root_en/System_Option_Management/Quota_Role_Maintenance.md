# Quota_Role_Maintenance

  #@img_SYS0005/image19.png

**[System Management-General].Quota Category: This function needs to be set only when "Points" is selected.**

**Print Quota Setting Note: When setting print quota, both the printing personnel and their department must have quota to be authorized to print.**

**[Add]：建立一個新的額度角色**

**Example: Create a general quota role normal_quota: 1000 points per month**

  #@img_SYS0005/image20.png

**Quota Role: Can be applied to user groups and departments.**

**新增後，EnterEdit詳細資料**

  #@img_SYS0005/image21.png

> **Reset Quota**：Reset user quota and department quota associated with this quota role.

  #@img_SYS0005/image22.png

> Application 1: User Group -- Quota used by this user group
>
> Application 2: Department -- Quota used by this department (Total department usage cannot exceed department quota)
>
> Application: User Group -- Control user print quota

  #@img_SYS0005/image23.png

> Users belonging to this user group apply the print quota of this quota role.
>
> Application: Department -- Control department print quota

  #@img_SYS0005/image24.png

> Control Department Print Quota: Total print usage of this department for the month cannot exceed print quota of the quota role.
