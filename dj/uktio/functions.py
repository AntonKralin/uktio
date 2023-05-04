def region_query_to_select(queryset):
    rez_list = []
    for i_elem in queryset:
        buf_tuple = (i_elem.id, i_elem.name)
        rez_list.append(buf_tuple)
    return rez_list

def organization_query_to_select(queryset):
    rez_list = []
    for i_elem in queryset:
        buf_tuple = (i_elem.id, i_elem.name)
        rez_list.append(buf_tuple)
    return rez_list