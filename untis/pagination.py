__author__ = 'Administrator'
from django.utils.safestring import mark_safe


class Page:
    def __init__(self, current_page, data_count, per_page_count=5, pager_num=5):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num

    @property#为了前面使用不带括号
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v

    def page_str(self, base_url):
        page_list = []

        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        if self.current_page == 1:
            prev = '<a style="padding:0 5px;margin:0 5px;" href="javascript:void(0);">上一页</a>'
        else:
            prev = '<a style="padding:0 5px;margin:0 5px;" href="%s&p=%s">上一页</a>' % (base_url, self.current_page - 1,)
        page_list.append(prev)

        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp = '<a style="padding:0 5px;margin:0 5px;" class="active" href="%s&p=%s">%s</a>' % (base_url, i, i)
            else:
                temp = '<a style="padding:0 5px;margin:0 5px;" href="%s&p=%s">%s</a>' % (base_url, i, i)
            page_list.append(temp)

        jump = """
                <input id='page_input' type="text" style="width: 20px;text-align: center"><a style="padding:0 5px;margin:0 5px;" href="javascript:void(0);" onclick='jumpTo(this, "%s&p=");'>GO</a>
                <script>
                    var page_input=document.getElementById('page_input');
                    page_input.value=1;
                    function jumpTo(ths,base){
                        var val = ths.previousSibling.value;
                        if (val<=0){
                            val = 1;
                        }else if (val>%s){
                            val = %s
                        }
                        location.href = base + val;
                    }
                </script>
                """ % (base_url, self.total_count, self.total_count)

        page_list.append(jump)

        if self.current_page == self.total_count:
            nex = '<a style="padding:0 5px;margin:0 5px;" href="javascript:void(0);">下一页</a>'
        else:
            nex = '<a style="padding:0 5px;margin:0 5px;" href="%s&p=%s">下一页</a>' % (base_url, self.current_page + 1,)
        page_list.append(nex)

        page_str = mark_safe("".join(page_list))

        return page_str
