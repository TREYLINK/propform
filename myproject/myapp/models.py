from django.db import models
from django.contrib.auth.models import User

class MultiSelectField(models.CharField):
    description = "複数選択可能な CharField"

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.get('choices')
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if isinstance(value, list):
            return ','.join(value)
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value.split(',')

class Developer(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    land_quantity = models.IntegerField(default=0)
    building_quantity = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    additional_requirements = models.TextField(blank=True, null=True)  # その他要求事項
    plan = models.CharField(max_length=10, choices=[('light', 'ライトプラン'), ('medium', 'ミディアムプラン'), ('premium', 'プレミアムプラン')], default='light',blank=True)  # プラン
    expected_contract_date = models.DateField(blank=True, null=True)  # 契約予定日
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)  # 添付ファイル
    def __str__(self):
        return f"({self.building_quantity}), ({self.land_quantity})"

# 土地
class Land(models.Model):
    田 = '田'
    畑 = '畑'
    宅地 = '宅地'
    塩田 = '塩田'
    鉱泉地 = '鉱泉地'
    池沼 = '池沼'
    山林 = '山林'
    牧場 = '牧場'
    原野 = '原野'
    墓地 = '墓地'
    境内地 = '境内地'
    運河用地 = '運河用地'
    水道用地 = '水道用地'
    用悪水路 = '用悪水路'
    ため池 = 'ため池'
    堤 = '堤'
    井溝 = '井溝'
    保安林 = '保安林'
    公衆用道路 = '公衆用道路'
    公園 = '公園'
    雑種地 = '雑種地'

    LAND_TYPE_CHOICES = [
        (田, '田'),
        (畑, '畑'),
        (宅地, '宅地'),
        (塩田, '塩田'),
        (鉱泉地, '鉱泉地'),
        (池沼, '池沼'),
        (山林, '山林'),
        (牧場, '牧場'),
        (原野, '原野'),
        (墓地, '墓地'),
        (境内地, '境内地'),
        (運河用地, '運河用地'),
        (水道用地, '水道用地'),
        (用悪水路, '用悪水路'),
        (ため池, 'ため池'),
        (堤, '堤'),
        (井溝, '井溝'),
        (保安林, '保安林'),
        (公衆用道路, '公衆用道路'),
        (公園, '公園'),
        (雑種地, '雑種地'),
    ]
    RIGHT_TYPE_CHOICES = [
        ('所有権', '所有権'),
        ('地上権', '地上権'),
        ('賃借権', '賃借権'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    address = models.CharField(max_length=255) # 所在地
    area = models.IntegerField(null=True, blank=True) # 面積
    real_estate_number = models.CharField(max_length=255, null=True, blank=True) # 不動産番号
    chimoku = models.CharField(max_length=10, choices=LAND_TYPE_CHOICES, default=田) # 地目
    chimoku_status = models.CharField(max_length=20, null=True, blank=True) # 地目_現況
    mochibun = models.CharField(max_length=20, null=True, blank=True) # 持分
    right = models.CharField(max_length=10, choices=RIGHT_TYPE_CHOICES, default='所有権') # 権利の種類

# 建物
class Building(models.Model):
    # 建物 種類 選択肢
    HOUSE = 'HOUSE'
    APARTMENT = 'APARTMENT'
    INN = 'INN'
    FACTORY = 'FACTORY'
    SHOP = 'SHOP'
    DOMITORY = 'DOMITORY'
    OFFICE = 'OFFICE'
    RESTRANT = 'RESTRANT'
    STARAGE = 'STARAGE'
    CARAGE = 'CARAGE'
    SCHOOL = 'SCHOOL'
    BANK = 'BANK'
    HOSPITAL = 'HOSPITAL'
    PARKING = 'PARKING'
    ETC = 'ETC'
    # 追加選択肢

    BUILDING_TYPE_CHOICES = [
        (HOUSE, '居宅'),
        (APARTMENT, '共同住宅'),
        (INN, '旅館'),
        (SHOP, '店舗'),
        (FACTORY, '工場'),
        (DOMITORY, '寄宿舎'),
        (OFFICE, '事務所'),
        (INN, '旅館'),
        (RESTRANT, '料理店'),
        (STARAGE, '倉庫'),
        (CARAGE, '車庫'),
        (SCHOOL, '校舎'),
        (BANK, '銀行'),
        (HOSPITAL, '病院'),
        (ETC, 'その他'),
        # 追加選択肢
    ]
    # building_name = models.CharField(max_length=255, null=True, blank=True)
    land_address = models.CharField(max_length=255, null=True, blank=True) # 所在
    house_number = models.CharField(max_length=255, null=True, blank=True) # 家屋番号
    real_estate_number = models.CharField(max_length=255, null=True, blank=True) # 不動産番号
    floor = models.IntegerField(null=True, blank=True) # 階数
    area_floor = models.IntegerField(null=True, blank=True) # 床面積
    building_type = models.CharField(max_length=10, choices=BUILDING_TYPE_CHOICES, default=HOUSE)
    # owner_name = models.CharField(max_length=255, null=True, blank=True) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

class Apartment(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=10)
    floor = models.IntegerField()
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.building.building_name} - {self.unit_number}"

class Buyer(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Contract(models.Model):
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE)
    contract_date = models.DateField()
    contract_amount = models.DecimalField(max_digits=12, decimal_places=2)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # 氏名
    company_name = models.CharField(max_length=100) # 商号又は名称
    cphone_number = models.CharField(max_length=15, null= True) # TEL_Company
    phone_number = models.CharField(max_length=15) # TEL_Private
    fax_number = models.CharField(max_length=15) # FAX
    address = models.CharField(max_length=255) # 主たる事務所所在地
    housenumber = models.CharField(max_length=50) # 屋号
    email = models.EmailField(max_length=50) # email
    name_leader = models.CharField(max_length=50)  # 代表者の氏名
    department = models.CharField(max_length=50) # 部署名
    company_number = models.CharField(max_length=50) # 会社法人等番号【登記簿記載】
    housing_license = models.CharField(max_length=50) # 免許証番号

    def __str__(self):
        return self.user.username

class Land_m(models.Model):
    STATUS_CHOICES = [
        ('baiuri','売買の売主'),
        ('baidai','売買の代理'),
        ('baibai','売買の媒介'),
        ('kouuri','交換の売主'),
        ('koudai','交換の代理'),
        ('koubai','交換の媒介'),
    ]
    OPTIONS = [
        ('kari_kanchi', '仮換地'),
        ('horyuchi_yoteichi', '保留地予定地'),
    ]
    SERVEY_OPTIONS = [
        ('kakutei','確定測量図'),
        ('genkyou','現況測量図'),
        ('chiseki','地積測量図'),
        ('etc','その他'),
    ]
    # 不動産入力
    user_A = models.ForeignKey('UserProfile', related_name='land_m_user_A', on_delete= models.CASCADE)
    user_B = models.ForeignKey('UserProfile', related_name='land_m_user_B', on_delete= models.CASCADE)

    # 土地情報入力
    land_1 = models.ForeignKey("Land", related_name='land_m_1', on_delete=models.CASCADE)
    land_2 = models.ForeignKey("Land", related_name='land_m_2', on_delete=models.CASCADE)
    land_3 = models.ForeignKey("Land", related_name='land_m_3', on_delete=models.CASCADE)
    land_4 = models.ForeignKey("Land", related_name='land_m_4', on_delete=models.CASCADE)
    land_5 = models.ForeignKey("Land", related_name='land_m_5', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True) # 取引態様
    total_area = models.IntegerField(null=True, blank=True)
    actual_total_area = models.IntegerField(null=True, blank=True)
    options = MultiSelectField(max_length=20, choices=OPTIONS, blank=True)
    survey_map = models.CharField(max_length=10, choices=SERVEY_OPTIONS, blank=True)
    survey_map_date = models.CharField(max_length=100)
    land_etc = models.TextField(blank=True)

    ######################### Ⅰ 対象となる宅地に直接関係する事項 ########################

    # 1 登記記録に記録された事項
    # 権利部（甲区）
    名義人住所 = models.CharField(max_length=255)
    名義人氏名 = models.CharField(max_length=255)
    所有権にかかる権利に関する事項_甲 = models.BooleanField(default=True)
    差押登記 = models.BooleanField(default=True)
    仮差押 = models.BooleanField(default=True)
    仮処分 = models.BooleanField(default=True)
    所有権移転仮登記 = models.BooleanField(default=True)

    # 権利部(乙区)
    所有権にかかる権利に関する事項_乙 = models.BooleanField(default=True)
    地上権 = models.BooleanField(default=True)
    抵当権 = models.BooleanField(default=True)
    根抵当権 = models.BooleanField(default=True)
    賃借権 = models.BooleanField(default=True)
    備考_1 = models.TextField(blank=True)


    # 2 借地権(使用貸借権)の売買等の場合
    該当_2 = models.BooleanField(default=True)
    説明書参照_2 = models.TextField(blank=True)

    # 3 第三者による対象物件の占有に関する事項
    第三者による占有 = models.BooleanField(default=True)
    占有者住所 = models.CharField(max_length=255)
    占有者氏名 = models.CharField(max_length=255)
    # 権利関係
    借地人 = models.BooleanField(default=True)
    賃貸借 = models.BooleanField(default=True)
    使用貸借 = models.BooleanField(default=False)
    blank_3 = models.BooleanField(default=False)
    blank_3_detail = models.CharField(max_length=255)
    
    備考_3 = models.TextField(blank=True)

    # 4 都市計画法・建築基準法等の法令に基づく制限の概要
    ######################### (1) 都市計画法・建築基準法に基づく制限の概要 ########################
    # ① 都市計画区域
    KUIKI_IN_OPTIONS = [
        ('SICHO','市街化区域'),
        ('SICHOCHOUSEI','市街化調整区域'),
        ('その他','線引きされていない区域'),
    ]
    KUIKI_OUT_OPTIONS = [
        ('JYUNTOSHI','準都市計画区域'),
        ('TOSHI','都市計画区域・準都市計画区域外'),
    ]
    # 区分区域
    区域区分_内 = models.CharField(max_length=20, choices=KUIKI_IN_OPTIONS, blank=True)
    区域区分_外 = models.CharField(max_length=20, choices=KUIKI_OUT_OPTIONS, blank=True)

    # 開発行為等の制限
    開発行為をする場合 = models.BooleanField(default=True)
    許可_maru1 = models.BooleanField(default=True)
    開発許可申請後の場合 = models.BooleanField(default=False)
    許可済_maru1 = models.BooleanField(default=False)
    開発行為完了の場合 = models.BooleanField(default=False)
    工場完了公告有無 = models.BooleanField(default=False)

    # ② 都市計画制限
    都市計画制限有無 = models.BooleanField(default=True)
    都市計画施設等の区域内 = models.BooleanField(default=True)
    都市計画事業の事業地内 = models.BooleanField(default=True)
    blank_maru2 = models.CharField(max_length=100, null=True, blank=True)
    計画事業名 = models.CharField(max_length=100, null=True, blank=True)
    date_maru2 = models.DateField(blank=True, null=True)

    # ③ 用途地域
    YOUTO_CHIIKI_OPTIONS = [
        ('A','第1種低層住居専用地域'),
        ('B','第2種低層住居専用地域'),
        ('C','第1種中高層住居専用地域'),
        ('D','第2種中高層住居専用地域'),
        ('E','第1種住居地域'),
        ('F','第2種住居地域'),
        ('G','準住居地域'),
        ('H','田園住居地域'),
        ('I','近隣商業地域'),
        ('J','商業地域'),
        ('K','準工業地域'),
        ('L','工業地域'),
        ('M','工業専用地'),
        ('Z',' '),
    ]
    用途地域_A = models.CharField(max_length=50, choices=YOUTO_CHIIKI_OPTIONS, default = 'Z')
    用途地域_B = models.CharField(max_length=50, choices=YOUTO_CHIIKI_OPTIONS, default = 'Z')

    # ④ 地区・街区等
    # 特別用途地区　特定用途制限地域
    特別用途地区 = models.BooleanField(default=False)
    特定用途制限地域 = models.BooleanField(default=False)
    blank_maru4_1 = models.CharField(max_length=50, blank=True, null=True)

    # その他の地域地区等
    高層主居誘導地球 = models.BooleanField(default=False)
    高度地区 = models.BooleanField(default=False)
    高度利用地区 = models.BooleanField(default=False)
    防火地域 = models.BooleanField(default=False)
    準防火地域 = models.BooleanField(default=False)
    特定防災街区整備地区 = models.BooleanField(default=False)
    風致地区 = models.BooleanField(default=False)
    blank_maru4_2 = models.CharField(max_length=50, blank=True, null=True)

    # ⑤ 建蔽率の制限
    指定建蔽率 = models.IntegerField(null=True, blank=True)
    建蔽率の緩和 = models.TextField(blank=True)
    
    # ⑥ 容積率の制限
    # a
    指定容積率 = models.IntegerField(null=True, blank=True)
    特殊容積率の適用 = models.BooleanField(default=False)
    特殊容積率 = models.IntegerField(blank=True, null=True)

    # b
    # 道路幅員制限(前面道路の幅員が12m未満の場合)
    幅員 = models.IntegerField(blank=True, null=True)
    特定道路による緩和 = models.IntegerField(blank=True, null=True)
    # ※掛け算数値リスト追加
    道路幅員制限 = models.IntegerField(blank=True, null=True)
    備考_4 = models.TextField(blank=True)

    # ⑧ 建築物の高さの制限
    YUMU_OPTIONS = [
        ('NONE',' '),
        ('YES','有'),
        ('NO','無')
    ]
    道路傾斜制限 = models.CharField(max_length=10, choices=YUMU_OPTIONS,default='NONE')
    隣地斜線制限 = models.CharField(max_length=10, choices=YUMU_OPTIONS,default='NONE')
    北側斜線制限 = models.CharField(max_length=10, choices=YUMU_OPTIONS,default='NONE')
    日影規制 = models.CharField(max_length=10, choices=YUMU_OPTIONS,default='NONE')
    絶対高さ制限 = models.CharField(max_length=10, choices={('NONE',' '), ('YES1','有(10m)'), ('YES2','有(12m)'), ('NO','無')},default='NONE')

    # ⑧ その他の建築制限
    外壁後退距離制限_c = models.BooleanField(default=False)
    外壁後退距離制限 = models.CharField(max_length=10, choices={('none',' '),('a','1.5m以上'),('b','1m以上')},default='none')
    敷地面積の制限_c = models.BooleanField(default=False)
    敷地面積の制限 = models.IntegerField(blank=True, null=True)

    # ⑨ 条例による制限その他の制限
    災害危険区域 = models.BooleanField(default=False)
    地区計画の区域 = models.BooleanField(default=False)
    建築協定区域 = models.BooleanField(default=False)
    建築協定区域 = models.BooleanField(default=False)
    blank_maru9_check = models.BooleanField(default=False)
    blank_maru9_text = models.TextField(blank=True)

    # ⑩ 敷地と道路との関係による制限
    # 敷地の接道義務
    幅員_maru10 = models.CharField(max_length=10, choices={('none',' '),('4','4m'),('6','6m')}, default='none')
    check_maru10 = models.BooleanField(default=False)
    路地状敷地の場合_check = models.BooleanField(default=False)
    路地状敷地の場合_text = models.TextField(blank=True)
    特殊建築物の場合_check = models.BooleanField(default=False)
    特殊建築物の場合_text = models.TextField(blank=True)
    blank_maru10_check = models.BooleanField(default=False)
    blank_maru10_text = models.TextField(blank=True)

    # 接道の状況
    接道方向_1 = models.CharField(max_length=10, null=True, blank=True)
    公私道の別_1 = models.CharField(max_length=10, choices={('none',' '),('koudo','公道'),('sidou','私道')}, default='none')
    接道道路種類_1 = models.CharField(max_length=10, choices={('none',' '),('a','ア'),('i','イ'),('u','ウ'),('e','エ'),('o','オ'),('ka','カ'),('ki','キ')}, default='none')
    幅員_maru10_1 = models.FloatField(blank=True, null=True)
    接道長さ_1 = models.FloatField(blank=True, null=True)

    接道方向_2 = models.CharField(max_length=10, null=True, blank=True)
    公私道の別_2 = models.CharField(max_length=10, choices={('none',' '),('koudo','公道'),('sidou','私道')}, default='none')
    接道道路種類_2 = models.CharField(max_length=10, choices={('none',' '),('a','ア'),('i','イ'),('u','ウ'),('e','エ'),('o','オ'),('ka','カ'),('ki','キ')}, default='none')
    幅員_maru10_2 = models.FloatField(blank=True, null=True)
    接道長さ_2 = models.FloatField(blank=True, null=True)

    接道方向_3 = models.CharField(max_length=10, null=True, blank=True)
    公私道の別_3 = models.CharField(max_length=10, choices={('none',' '),('koudo','公道'),('sidou','私道')}, default='none')
    接道道路種類_3 = models.CharField(max_length=10, choices={('none',' '),('a','ア'),('i','イ'),('u','ウ'),('e','エ'),('o','オ'),('ka','カ'),('ki','キ')}, default='none')
    幅員_maru10_3 = models.FloatField(blank=True, null=True)
    接道長さ_3 = models.FloatField(blank=True, null=True)

    # 道路の種類
    指定番号_年号 = models.CharField(max_length=10, choices={('none',' '),('s','昭和'),('h','平成'),('r','令和')},default = 'none')
    指定番号_日付 = models.DateField(blank=True, null=True)
    指定番号 = models.IntegerField(blank=True, null=True)
    カ_項目 = models.CharField(max_length=10, choices=[('2','2m'),('3','3m'),('none',' ')], default='none')

    備考_maru10 = models.TextField(blank=True)

    # ⑪ 敷地と道路の関係図
    敷地と道路との関係図 = models.FileField(upload_to='documents/')

    # ⑬ 私道にかかる制限
    maru12 = models.BooleanField(default=False)


    ###################### (2)都市計画法・建築基準法以外の法令に基づく制限の概要 ########################
    # ①
    # 法令名
    古都保存法 = models.BooleanField(default=False)
    都市緑地法 = models.BooleanField(default=False)
    生産緑地法 = models.BooleanField(default=False)
    特定空港周辺特別措置法 = models.BooleanField(default=False)											
    景観法 = models.BooleanField(default=False)											
    大都市地域における住宅及び住宅地の供給の促進に関する特別措置法 = models.BooleanField(default=False)											
    地方拠点都市地域の整備及び産業業務施設の再配置の促進に関する法律 = models.BooleanField(default=False)											
    被災市街地復興特別措置法 = models.BooleanField(default=False)											
    新住宅市街地開発法 = models.BooleanField(default=False)											
    新都市基盤整備法 = models.BooleanField(default=False)											
    旧市街地改造法 = models.BooleanField(default=False)											
    首都圏の近郊整備地帯及び都市開発区域の整備に関する法律 = models.BooleanField(default=False)											
    近畿圏の近郊整備区域及び都市開発区域の整備及び開発に関する法律 = models.BooleanField(default=False)											
    流通業務市街地整備法 = models.BooleanField(default=False)											
    都市再開発法 = models.BooleanField(default=False)											
    沿道整備法 = models.BooleanField(default=False)											
    集落地域整備法 = models.BooleanField(default=False)											
    密集市街地における防災街区の整備の促進に関する法律 = models.BooleanField(default=False)											
    地域における歴史的風致の維持及び向上に関する法律 = models.BooleanField(default=False)											
    港湾法 = models.BooleanField(default=False)											
    住宅地区改良法 = models.BooleanField(default=False)											
    農地法 = models.BooleanField(default=False)											
    宅地造成及び特定盛土等規制法 = models.BooleanField(default=False)											
    マンション建替え円滑化法 = models.BooleanField(default=False)											
    長期優良住宅の普及の促進に関する法律 = models.BooleanField(default=False)											
    都市公園法 = models.BooleanField(default=False)											
    自然公園法 = models.BooleanField(default=False)											
    首都圏近郊緑地保全法 = models.BooleanField(default=False)											
    近畿圏の保全区域の整備に関する法律 = models.BooleanField(default=False)											
    都市の低炭素化の促進に関する法律 = models.BooleanField(default=False)											
    水防法 = models.BooleanField(default=False)											
    下水道法 = models.BooleanField(default=False)											
    河川法 = models.BooleanField(default=False)											
    特定都市河川浸水被害対策法 = models.BooleanField(default=False)											
    海岸法 = models.BooleanField(default=False)											
    津波防災地域づくりに関する法律 = models.BooleanField(default=False)											
    砂防法 = models.BooleanField(default=False)											
    地すべり等防止法 = models.BooleanField(default=False)											
    急傾斜地法 = models.BooleanField(default=False)											
    森林法 = models.BooleanField(default=False)											
    森林経営管理法 = models.BooleanField(default=False)											
    道路法 = models.BooleanField(default=False)											
    踏切道改良促進法 = models.BooleanField(default=False)											
    全国新幹線鉄道整備法 = models.BooleanField(default=False)											
    土地収用法 = models.BooleanField(default=False)											
    文化財保護法 = models.BooleanField(default=False)											
    航空法 = models.BooleanField(default=False)											
    国土利用計画法 = models.BooleanField(default=False)											
    廃棄物の処理及び清掃に関する法律 = models.BooleanField(default=False)											
    土壌汚染対策法 = models.BooleanField(default=False)											
    都市再生特別措置法 = models.BooleanField(default=False)											
    地域再生法 = models.BooleanField(default=False)											
    高齢者障害者等の移動等の円滑化の促進に関する法律 = models.BooleanField(default=False)											
    災害対策基本法 = models.BooleanField(default=False)											
    東日本大震災復興特別区域法 = models.BooleanField(default=False)											
    大規模災害からの復興に関する法律 = models.BooleanField(default=False)											
    重要土地等調査法 = models.BooleanField(default=False)	

    # 制限の内容
    制限の内容_maru1 = models.TextField(blank=True)										

    備考_maru1 = models.TextField(blank=True)

    # ②　土地区画整理法
    区画整理 = models.CharField(max_length=10, choices=[('keikakuari','計画有'),('sikochu','試行中'),('none',' ')], default='none')
    区画整理名称 = models.CharField(max_length=50, null=True, blank=True)
    # 仮換地指定										
    仮換地指定= models.BooleanField(default=False) # True = 済, False = 未
    仮換地指定_date = models.DateField(blank=True, null=True)
    仮換地指定_号 = models.IntegerField(blank=True, null=True)
    
    換地処分公告日_予定 = models.DateField(blank=True, null=True)

    清算金_有 = models.BooleanField(default=False)
    清算金_無 = models.BooleanField(default=False)
    清算金_未定 = models.BooleanField(default=False)
    清算金_確定 = models.BooleanField(default=False)
    清算金_確定 = models.IntegerField(blank=True, null=True)
    清算金_交付 = models.BooleanField(default=False)
    清算金_徴収 = models.BooleanField(default=False)

    賦課金_有 = models.BooleanField(default=False)
    賦課金_確定 = models.BooleanField(default=False)
    賦課金_確定 = models.IntegerField(blank=True, null=True)
    賦課金_無 = models.BooleanField(default=False)
    賦課金_未定 = models.BooleanField(default=False)

    制限の内容_maru2 = models.TextField(blank=True)

    # 5 私道の負担に関する事項(私道がある場合：「敷地と道路との関係図」参照)
    負担 = models.BooleanField(default=False)
    備考_5 = models.TextField(blank=True)

    # 6 当該宅地が造成宅地防災区域内か否か
    造成宅地防災区域_外 = models.BooleanField(default=False)
    造成宅地防災区域_内 = models.BooleanField(default=False)

    # 7 当該宅地が土砂災害警戒区域内か否か
    土砂災害警戒区域_外 = models.BooleanField(default=False)
    土砂災害警戒区域_内 = models.BooleanField(default=False)
    土砂災害特別警戒区域_外 = models.BooleanField(default=False)
    土砂災害特別警戒区域_内 = models.BooleanField(default=False)

    # 8 当該宅地が津波災害警戒区域内か否か
    津波災害警戒区域_外 = models.BooleanField(default=False)
    津波災害警戒区域_内 = models.BooleanField(default=False)
    津波災害警戒区域_未指定 = models.BooleanField(default=False)
    津波災害特別警戒区域_外 = models.BooleanField(default=False)
    津波災害特別警戒区域_内 = models.BooleanField(default=False)

    # 9 水防法施行規則の規定により市町村の長が提供する図面（水害ハザードマップ）における当該宅地の所在地
    # 水害ハザードマップの有無
    洪水_有 = models.BooleanField(default=False)
    洪水_図面名称 = models.CharField(max_length=20, blank=True, null=True)
    洪水_無 = models.BooleanField(default=False)
    洪水_照会先 = models.CharField(max_length=20, blank=True, null=True)

    雨水出水_有 = models.BooleanField(default=False)
    雨水出水_図面名称 = models.CharField(max_length=20, blank=True, null=True)
    雨水出水_無 = models.BooleanField(default=False)
    雨水出水_照会先 = models.CharField(max_length=20, blank=True, null=True)

    高潮_有 = models.BooleanField(default=False)
    高潮_図面名称 = models.CharField(max_length=20, blank=True, null=True)
    高潮_無 = models.BooleanField(default=False)
    高潮_照会先 = models.CharField(max_length=20, blank=True, null=True)

    # 水害ハザードマップにおける宅地の所在地
    該当_9 = models.BooleanField(default=False)
    該当_9_text = models.TextField(blank=True)

    備考_9 = models.TextField(blank=True)

    # 10 飲用水・ガス･電気の供給施設及び排水施設の整備状況
    # A 直ちに利用可能な施設 B 配管等の状況 C 整備予定・負担金予定額 
    # ① 食用水
    食用水_A = models.CharField(max_length=10, choices=[('suidokou','水道(公営)'),('suidosi','水道(私営)'),('ido','井戸'),('nashi','無'),('none',' ')],default='none')
    
    前面道路配管_食用水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')
    前面道路配管口径_食用水 = models.FloatField(blank=True, null=True)
    敷地内引込管_食用水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')
    敷地内引込管口径_食用水 = models.FloatField(blank=True, null=True)
    私設管の有無_食用水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')

    日付_食用水_C = models.DateField(blank=True, null=True)
    食用水_C = models.BooleanField(default=False)
    金額_食用水_C = models.IntegerField(blank=True, null=True)

    # ② ガス
    ガス_A = models.CharField(max_length=10, choices=[('tosi','都市ガス'),('puroko','プロパン(個別)'),('purosyu','プロパン(集中)'),('nashi','無'),('none',' ')],default='none')
    ガス会社名_A = models.CharField(max_length=10, blank=True, null=True)
    
    前面道路配管_ガス = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')
    前面道路配管口径_ガス = models.FloatField(blank=True, null=True)
    敷地内引込管_ガス = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')
    
    日付_ガス_C = models.DateField(blank=True, null=True)
    ガス_C = models.BooleanField(default=False)
    金額_ガス_C = models.IntegerField(blank=True, null=True)

    ガス_check = models.BooleanField(default=False)
    ガス_detail = models.TextField(blank=True)

    # ③ 電気
    電気_有 = models.BooleanField(default=False)
    電気_小売電気事業者 = models.CharField(max_length=20, blank=True, null=True)
    電気_住所 = models.CharField(max_length=30, blank=True, null=True)
    電気_電話 = models.CharField(max_length=20, blank=True, null=True)
    電気_無 = models.BooleanField(default=False)

    日付_電気_C = models.DateField(blank=True, null=True)
    電気_C = models.BooleanField(default=False)
    金額_電気_C = models.IntegerField(blank=True, null=True)

    # ④ 汚水
    汚水_A = models.CharField(max_length=10, choices=[('kokyogesui','公共下水'),('gappei','個別浄化槽(合併)'),('tandoku','個別浄化槽(単独)'),('syuchu','集中浄化槽'),('suitori','汲取式'),('nashi','無'),('none',' ')],default='none')
    
    前面道路配管_汚水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')
    私設管の有無_汚水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')
    浄化槽施設の必要_汚水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')

    日付_汚水_C = models.DateField(blank=True, null=True)
    汚水_C = models.BooleanField(default=False)
    金額_汚水_C = models.IntegerField(blank=True, null=True)

    # ⑤ 雑排水
    雑排水_A = models.CharField(max_length=10, choices=[('kokyogesui','公共下水'),('gappei','個別浄化槽(合併)'),('tandoku','個別浄化槽(単独)'),('syuchu','集中浄化槽'),('sintou','浸透式'),('sokukou','側溝等'),('nashi','無'),('none',' ')],default='none')
    
    前面道路配管_雑排水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')
    私設管の有無_雑排水 = models.CharField(max_length=10, choices=YUMU_OPTIONS, default='NONE')

    日付_雑排水_C = models.DateField(blank=True, null=True)
    雑排水_C = models.BooleanField(default=False)
    金額_雑排水_C = models.IntegerField(blank=True, null=True)

    # ⑥ 雨水
    雨水_A = models.CharField(max_length=10, choices=[('kokyogesui','公共下水'),('sintou','浸透'),('sokukou','側溝'),('nashi','無'),('none',' ')],default='none')
    
    日付_雨水_C = models.DateField(blank=True, null=True)
    雨水_C = models.BooleanField(default=False)
    金額_雨水_C = models.IntegerField(blank=True, null=True)

    備考_10 = models.TextField(blank=True)

    # 11 宅地造成の工事完了時における形状・構造等(未完成物件等の場合）
    該当_11 = models.BooleanField(default=False)

    ######################## 取引条件に関する事項 ########################

    # １ 代金・交換差金及び地代に関する事項   
    # 売買代金
    土地価格総額 = models.IntegerField(blank=True, null=True)

    # 交換差金
    支払う = models.BooleanField(default=False)
    受領する = models.BooleanField(default=False)
    交換差金_差金 = models.IntegerField(blank=True, null=True)
    交換差金_内消費税等 = models.IntegerField(blank=True, null=True)

    # 地代
    地代金 = models.IntegerField(blank=True, null=True)

    # ２ 代金・交換差金以外に授受される金銭の額及び授受の目的
    # 授受の目的
    手付金_金額 = models.IntegerField(blank=True, null=True)

    固定資産税等_date = models.CharField(max_length=10, choices=[('A','1月1日'),('B','4月1日'),('none',' ')], default='none')
    固定資産税等_金額 = models.IntegerField(blank=True, null=True)
    
    授受目的_A = models.CharField(max_length=100, blank=True, null=True)
    授受目的_A_金額 = models.IntegerField(blank=True, null=True)
    授受目的_A_消費税 = models.IntegerField(blank=True, null=True)

    授受目的_B = models.CharField(max_length=100, blank=True, null=True)
    授受目的_B_金額 = models.IntegerField(blank=True, null=True)
    授受目的_B_消費税 = models.IntegerField(blank=True, null=True)
    
    授受目的_C = models.CharField(max_length=100, blank=True, null=True)
    授受目的_C_金額 = models.IntegerField(blank=True, null=True)
    授受目的_C_消費税 = models.IntegerField(blank=True, null=True)

    授受目的_D = models.CharField(max_length=100, blank=True, null=True)
    授受目的_D_金額 = models.IntegerField(blank=True, null=True)
    授受目的_D_消費税 = models.IntegerField(blank=True, null=True)

    備考_2_2 = models.TextField(blank=True)

    # ３ 契約の解除に関する事項(契約書(案)添付のうえ説明)
    # 手付解除
    事項1 = models.BooleanField(default=False)
    事項1_条 = models.IntegerField(blank=True, null=True)
    
    # 引渡前の滅失・損傷の場合の解除
    事項2 = models.BooleanField(default=False)
    事項2_条 = models.IntegerField(blank=True, null=True)

    # 契約違反による解除
    事項3 = models.BooleanField(default=False)
    事項3_条 = models.IntegerField(blank=True, null=True)

    # 反社会的勢力の排除条項に基づく解除
    事項4 = models.BooleanField(default=False)
    事項4_条 = models.IntegerField(blank=True, null=True)

    # 融資利用の特約による解除
    事項5 = models.BooleanField(default=False)
    事項5_条 = models.IntegerField(blank=True, null=True)
    
    # 契約不適合責任による解除
    事項6 = models.BooleanField(default=False)
    事項6_条 = models.IntegerField(blank=True, null=True)

    # 借地権譲渡について土地賃貸人の承諾を得ることを条件とする契約条項の場合
    事項7 = models.BooleanField(default=False)
    事項7_条 = models.IntegerField(blank=True, null=True)

    # 追加事項
    事項8 = models.TextField(blank=True)
    事項8_条 = models.TextField(blank=True)

    # ４ 損害賠償額の予定又は違約金に関する事項(契約書(案)添付のうえ説明）
    # 損害賠償額の予定又は違約金に関する定め
    定め_4_有 = models.BooleanField(default=False)
    定め_4_条1 = models.IntegerField(blank=True, null=True)
    定め_4_条1 = models.IntegerField(blank=True, null=True)
    定め_4_無 = models.BooleanField(default=False)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField()

class Report(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title