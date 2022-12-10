import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    is_active = models.BooleanField()


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=150)
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True, max_length=254, blank=True)
    phone_number = models.CharField(unique=True, max_length=30, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    user_created = models.CharField(max_length=150)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)
    last_login = None
    first_name = None
    last_name = None
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, related_name='users')


class TypeCategory(models.Model):
    type_name = models.CharField(max_length=150)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class Category(models.Model):
    parent = models.ForeignKey('self', models.SET_NULL, null=True, related_name="children")
    level = models.IntegerField()
    type = models.ForeignKey(TypeCategory, models.SET_NULL, null=True, related_name="category_type")
    state = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)
    group_product = models.ManyToManyField('GroupProduct', through='CategoryGroupProductLink', related_name='link')

    @property
    def active_children(self):
        return self.children.filter(state=True)


class CategoryDictionary(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='categorydictionary')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    translation = models.TextField(unique=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class GroupProduct(models.Model):
    level = models.IntegerField()
    ex_system_code_group = models.CharField(max_length=150)
    ex_system_code_parent_id = models.CharField(max_length=150, null=True)
    parent = models.ForeignKey('self', models.SET_NULL, null=True, related_name="children")
    state = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def active_children(self):
        return self.children.filter(state=True)


class GroupProductDictionary(models.Model):
    group_product = models.ForeignKey(GroupProduct, on_delete=models.SET_NULL, null=True,
                                      related_name='groupproductdictionary')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    translation = models.TextField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class CategoryGroupProductLink(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    group_product = models.ForeignKey(GroupProduct, on_delete=models.SET_NULL, null=True)
    state = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class Role(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    state = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)
    right = models.ManyToManyField('Right', through='RightForRole', related_name='rights')


class Right(models.Model):
    name = models.CharField(max_length=150)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class RightForRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    right = models.ForeignKey(Right, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class Cluster(models.Model):
    name = models.CharField(max_length=150)
    date_start = models.DateField()
    date_end = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    assort_matrix = models.ForeignKey('AssortMatrix', on_delete=models.SET_NULL, null=True)
    link_to_sp = models.CharField(max_length=15, null=True)
    is_actual = models.BooleanField(default=True)
    positioning = models.ForeignKey('Positioning', on_delete=models.SET_NULL, null=True)
    abbreviation = models.CharField(max_length=150)
    length_from = models.DecimalField(max_digits=10, decimal_places=1)
    length_to = models.DecimalField(max_digits=10, decimal_places=1)
    parent_cluster = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None)
    is_used_by_sp = models.BooleanField(default=False)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)
    shop = models.ManyToManyField('Shop', through='ClusterShopLink', related_name='shops')


class Shop(models.Model):
    ex_system_code_shop_id = models.CharField(max_length=150)
    ex_system_code_group_shop = models.CharField(max_length=150, null=True)
    shop_group = models.ForeignKey('GroupShops', models.SET_NULL, null=True, related_name='shops')
    count_of_opens = models.IntegerField(null=True)
    physical_address = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=254, blank=False)
    effective_from = models.DateField(null=True)
    shop_type = models.IntegerField()
    effective_to = models.DateField(null=True)
    city = models.CharField(max_length=150, null=True)
    state = models.CharField(max_length=150, null=True)
    country = models.CharField(max_length=150, null=True)
    latitude = models.CharField(max_length=150, null=True)
    longitude = models.CharField(max_length=150, null=True)
    total_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    merch_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_active = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)
    assort = models.ManyToManyField('Assort', through='AssortAction', related_name='assort')


class GroupShops(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', models.SET_NULL, null=True, related_name="children")
    ex_system_code_parent_id = models.CharField(max_length=150, null=True)
    ex_system_code_group_id = models.CharField(max_length=150)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ClusterShopLink(models.Model):
    cluster = models.ForeignKey(Cluster, models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    date_start = models.DateField()
    date_end = models.DateField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class Positioning(models.Model):
    name = models.CharField(max_length=150)


class AssortMatrix(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, models.SET_NULL, null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def order_by_id(self):
        return self.cluster_set.order_by('pk')


class Article(models.Model):
    ex_system_code_article = models.CharField(max_length=150)
    link_to_website = models.CharField(max_length=250, null=True)
    barcode_main = models.CharField(max_length=150, null=True)
    main_stock_unit = models.IntegerField(null=True)
    main_manufacturer = models.CharField(max_length=150, null=True)
    msu_manag = models.IntegerField(null=True)
    brand = models.CharField(max_length=150, null=True)
    extdesc1 = models.CharField(max_length=150, null=True)
    extdesc2 = models.CharField(max_length=150, null=True)
    extdesc3 = models.CharField(max_length=150, null=True)
    extdesc4 = models.CharField(max_length=150, null=True)
    extdesc5 = models.CharField(max_length=150, null=True)
    group_product = models.ForeignKey('GroupProduct', on_delete=models.PROTECT)
    stock_unit = models.ManyToManyField('StockUnit', through='ArticleStockUnit', related_name='stock_unit')
    unit_of_need = models.ManyToManyField('UnitOfNeed', through='ArticleUnitOfNeed', related_name='unit_of_need')
    ex_system_code_group_product = models.CharField(max_length=150)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ArticleUnitOfNeed(models.Model):
    article = models.ForeignKey(Article, models.SET_NULL, null=True)
    unit_of_need = models.ForeignKey('UnitOfNeed', models.SET_NULL, null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    state = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class UnitOfNeed(models.Model):
    article = models.ManyToManyField(Article, through='ArticleUnitOfNeed')
    name = models.CharField(max_length=150)
    ex_system_code_unit_of_need = models.CharField(max_length=150)
    state = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ArticleStockUnit(models.Model):
    article = models.ForeignKey('Article', on_delete=models.PROTECT)
    barcode = models.CharField(max_length=150, null=True)
    stock_unit = models.ForeignKey('StockUnit', on_delete=models.PROTECT)
    unit_of_need_code = models.IntegerField(null=True)
    is_base_unit = models.IntegerField(null=True)
    picture_link = models.CharField(max_length=150, null=True)
    coef_to_base_unit = models.IntegerField()
    ex_system_code_stock_unit = models.CharField(max_length=150)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ArticleStockUnitDictionary(models.Model):
    article_stock_unit = models.ForeignKey(ArticleStockUnit, on_delete=models.SET_NULL, null=True,
                                           related_name='articlstockunitdictionary')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    translation = models.TextField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class StockUnit(models.Model):
    ex_system_code_unit = models.CharField(max_length=15)
    stock_unit_desc = models.CharField(max_length=15)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ArticleWeightAndSize(models.Model):
    article_stock_unit = models.ForeignKey('ArticleStockUnit', models.SET_NULL, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    unit_of_measure_size = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    unit_of_weight_measure = models.IntegerField(null=True)
    unit_of_need = models.IntegerField(null=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class PurchasePricesAssort(models.Model):
    article_stock_unit = models.ForeignKey(ArticleStockUnit, models.SET_NULL, null=True)
    supplier = models.ForeignKey('Supplier', models.SET_NULL, null=True)
    purchase_price = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    is_main_supplier = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class Supplier(models.Model):
    ex_system_code_supplier_id = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    is_import = models.BooleanField(default=True)
    supplier_type = models.IntegerField()
    is_active = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class Supply(models.Model):
    ex_system_code_supply = models.CharField(max_length=15)
    article_id = models.IntegerField()
    article_unit_id = models.IntegerField()
    shop = models.ForeignKey(Shop, models.SET_NULL, null=True)
    qte = models.DecimalField(max_digits=10, decimal_places=3)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    delivery_date = models.DateField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ArticleStock(models.Model):
    article_id = models.IntegerField()
    article_stock_unit = models.ForeignKey('ArticleStockUnit', models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, models.SET_NULL, null=True)
    state = models.BooleanField(default=True)
    qte = models.DecimalField(max_digits=5, decimal_places=3)
    date_of_stock = models.DateField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ArticleSalesPrice(models.Model):
    article_id = models.IntegerField()
    shop = models.ForeignKey(Shop, models.SET_NULL, null=True)
    article_stock_unit = models.ForeignKey('ArticleStockUnit', models.SET_NULL, null=True)
    is_promotion_price = models.BooleanField()
    state = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=3)
    date_start = models.DateField()
    date_finish = models.DateField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class ArticleSales(models.Model):
    article_id = models.IntegerField()
    article_stock_unit = models.ForeignKey('ArticleStockUnit', models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, models.SET_NULL, null=True)
    qte = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    type_of_sales = models.IntegerField()
    state = models.BooleanField()
    date_of_sales = models.DateTimeField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class AssortAction(models.Model):
    assort = models.ForeignKey('Assort', models.SET_NULL, null=True)
    article_id = models.IntegerField()
    cluster_id = models.IntegerField()
    category_id = models.IntegerField()
    state = models.IntegerField()
    stock = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    ex_system_code_article = models.CharField(max_length=150)
    article_stock_unit_id = models.IntegerField()
    shop = models.ForeignKey('Shop', on_delete=models.PROTECT)
    action_type = models.IntegerField(null=True)
    action_group_type = models.IntegerField(null=True)
    date_start = models.DateField()
    date_finish = models.DateField()
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class Assort(models.Model):
    article = models.ForeignKey('Article', on_delete=models.PROTECT)
    ex_system_code_article_stock_unit = models.CharField(max_length=150)
    article_stock_unit = models.ForeignKey('ArticleStockUnit', on_delete=models.PROTECT)
    actual_assort_state = models.ForeignKey('AssortState', on_delete=models.PROTECT)
    cluster = models.ForeignKey('Cluster', models.SET_NULL, null=True)
    matrix_id = models.IntegerField(null=True)
    category_id = models.IntegerField(null=True)
    shop_id = models.IntegerField()
    unit_of_need_code = models.IntegerField(null=True)
    ex_system_code_unit_of_need = models.CharField(max_length=150)
    assort_operation = models.ForeignKey('AssortOperation', on_delete=models.PROTECT)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class AssortOperation(models.Model):
    operation_state = models.IntegerField()
    article_stock_unit_id = models.IntegerField()
    cluster_id = models.IntegerField(null=True)
    matrix_id = models.IntegerField()
    category_id = models.IntegerField(null=True)
    shop_id = models.IntegerField(null=True)
    action = models.ForeignKey('AssortActionList', on_delete=models.PROTECT)
    unit_of_need_code = models.IntegerField(default=0, null=True)
    assort_state = models.IntegerField()
    error_code = models.IntegerField(null=True, default=None)
    error_message = models.TextField(null=True, default=None)
    date_start = models.DateTimeField(auto_now=True)
    date_end = models.DateTimeField(auto_now=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class AssortActionList(models.Model):
    action_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class AssortState(models.Model):
    is_intermediate = models.BooleanField()
    is_actual = models.BooleanField()
    assort_group_state = models.ForeignKey('AssortGroupState', models.SET_NULL, null=True)
    color = models.CharField(max_length=50)


class AssortStateDictionary(models.Model):
    assort_state = models.ForeignKey(AssortState, on_delete=models.SET_NULL, null=True,
                                     related_name='assort_state_dictionary')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    translation = models.TextField(unique=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


class AssortGroupState(models.Model):
    is_actual = models.BooleanField()
    action_id = models.IntegerField()


class AssortGroupStateDictionary(models.Model):
    assort_group_state = models.ForeignKey(AssortGroupState, on_delete=models.SET_NULL, null=True,
                                           related_name='assort_group_state_dictionary')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    translation = models.TextField(unique=True)
    user_created = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.CharField(max_length=150)
    date_updated = models.DateTimeField(auto_now=True)


# class PlanogramList(models.Model):
#     planogram_code = models.TextField()
#     assort_id = models.IntegerField()
#     cluster_id = models.IntegerField()
#     shop_id = models.IntegerField()
#     article_id = models.IntegerField()
#     ex_system_code_article_id = models.CharField(max_length=150)
#     article_stock_unit_id = models.IntegerField()
#     ex_system_code_article_stock_unit_id = models.CharField(max_length=150)
#     is_active = models.BooleanField(default=True)
#     count_facing = models.IntegerField()
#     user_created = models.CharField(max_length=150)
#     date_created = models.DateTimeField(auto_now_add=True)
#     user_updated = models.CharField(max_length=150)
#     date_updated = models.DateTimeField(auto_now=True)
