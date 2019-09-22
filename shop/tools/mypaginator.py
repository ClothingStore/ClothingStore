from django.core.paginator import Paginator


class MyPaginator(Paginator):
    def __init__(self,object_list, per_page, orphans=0,
                 allow_empty_first_page=True,number=1):
        #number表示当前页
        super().__init__(object_list, per_page, orphans,allow_empty_first_page)
        self.number = self.validate_number(number)
    #改写父类的page_range属性，实现每页最多10个页码
    @property
    def page_range(self):
        #总页数小于10,返回所有的页码
        if self.num_pages <= 10:
            return range(1,self.num_pages+1)
        if self.number <= 6:
            return range(1,11)
        elif self.number + 4 <= self.num_pages:  #当前页加4小于等于总页数
            return range(self.number-5,self.number+5)
        else:
            return range(self.num_pages-9,self.num_pages+1)

    def page(self):
        return super().page(self.number)