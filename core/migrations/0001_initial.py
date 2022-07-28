# Generated by Django 2.2.10 on 2020-12-09 12:20

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=500)),
                ('apartment_address', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('zip', models.CharField(max_length=100)),
                ('address_type', models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1)),
                ('phone', models.CharField(default=False, max_length=15)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='images/ads/')),
                ('urlf', models.URLField(default='https://www.presimax.online/')),
                ('display', models.CharField(choices=[('D', 'Display'), ('N', 'Hide')], default='D', max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Ads',
            },
        ),
        migrations.CreateModel(
            name='Carousal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(null=True, upload_to='images/')),
                ('head', models.CharField(max_length=15)),
                ('des', models.CharField(max_length=100)),
                ('urlf', models.URLField()),
                ('color', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger'), ('I', 'indigo'), ('G', 'success'), ('B', 'blue')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='CarousalClub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(null=True, upload_to='images/')),
                ('head', models.CharField(max_length=15)),
                ('des', models.CharField(max_length=100)),
                ('urlf', models.URLField()),
                ('color', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger'), ('I', 'indigo'), ('G', 'success'), ('B', 'blue')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='CarousalEcommerce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(null=True, upload_to='images/')),
                ('head', models.CharField(max_length=15)),
                ('des', models.CharField(max_length=100)),
                ('urlf', models.URLField()),
                ('color', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger'), ('I', 'indigo'), ('G', 'success'), ('B', 'blue')], max_length=1)),
                ('position', models.CharField(choices=[('T', 'TOP'), ('M', 'MIDDLE'), ('B', 'BOTTOM')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=30)),
                ('link', models.URLField()),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Clickables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Clickables',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FAQs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=50)),
                ('answer', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('tag', models.CharField(blank=True, default='New', max_length=10, null=True)),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('club_discount_price', models.FloatField(blank=True, default=100000, null=True)),
                ('dis_per', models.FloatField(blank=True, default=-1, null=True)),
                ('category', models.CharField(choices=[('H', 'Handicrafts'), ('SS', 'Sarees'), ('G', 'Grocery'), ('P', 'Daily Needs'), ('FW', 'Fashion Wear'), ('F', 'Foot Wear'), ('FU', 'Furniture'), ('MW', 'MensWear'), ('BC', 'Beauty Care'), ('E', 'Electronics'), ('MA', 'Mens Accessories'), ('WA', 'Womens Accessories'), ('MP', 'Mobiles and Mobile accessories'), ('HA', 'Home Appliances'), ('S', 'Sports'), ('HC', 'Health Care'), ('KW', 'Kids Wear'), ('B', 'Books'), ('AA', 'Auto Accessories'), ('J', 'Jewellery')], max_length=2)),
                ('label', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger'), ('I', 'indigo'), ('G', 'success'), ('B', 'blue')], max_length=1)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('pweight', models.FloatField(default=-1)),
                ('pincode', models.IntegerField(default=123456)),
                ('schargeinc', models.FloatField(blank=True, default=-1, null=True)),
                ('club_schargeinc', models.FloatField(blank=True, default=-1, null=True)),
                ('has_size', models.BooleanField(blank=True, default=False, null=True)),
                ('rating', models.FloatField(blank=True, default=0, null=True)),
                ('COD', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Multiple_Pics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(blank=True, choices=[('BN', 'Buy Now'), ('S', 'Save')], max_length=20, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('mocreated', models.BooleanField(default=False)),
                ('payment', models.CharField(blank=True, choices=[('P', 'Paytm'), ('C', 'Cash On Delivery')], default=False, max_length=5, null=True)),
                ('being_delivered', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('refund_requested', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='core.Address')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Coupon')),
            ],
        ),
        migrations.CreateModel(
            name='Pagebackground',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/backgrounds/')),
                ('font_color', models.CharField(default='#000', max_length=10)),
                ('page', models.CharField(choices=[('H', 'Home'), ('C', 'Category'), ('S', 'Sales')], default='H', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Productbackground',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(default='#fdde6c', max_length=10)),
                ('font_color', models.CharField(default='#fff', max_length=10)),
                ('category_font_color', models.CharField(default='#fff', max_length=10)),
                ('page', models.CharField(choices=[('H', 'Home'), ('C', 'Category'), ('S', 'Sales')], default='H', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Sizes_class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizes_choice', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=5, null=True), blank=True, default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='TravelDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('spoint', models.CharField(max_length=20)),
                ('epoint', models.CharField(max_length=20)),
                ('phonenumber', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('carmodel', models.CharField(max_length=30)),
                ('carcapacity', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'TravelDetails',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Isclubmem', models.BooleanField(default=False)),
                ('userphoto', models.ImageField(null=True, upload_to='images/')),
                ('phone_number', models.CharField(default=False, max_length=30)),
                ('paid_amt', models.CharField(default='0', max_length=5)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('granted', models.BooleanField(default=False)),
                ('at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('checksum', models.CharField(blank=True, max_length=100, null=True)),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='HKR', max_length=20)),
                ('img', models.ImageField(upload_to='')),
                ('desig', models.CharField(default='CEO', max_length=20)),
                ('opinion', models.TextField()),
                ('team', models.CharField(blank=True, default=False, max_length=30, null=True)),
                ('facebook', models.URLField()),
                ('twitter', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_team', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_name', models.CharField(choices=[('DOD', 'Deals of the day'), ('FO', 'Flashsale On'), ('DS', 'Sunday Sale'), ('DOW', 'Deals of this week'), ('GDO', 'Great Discounts on')], max_length=30)),
                ('caption', models.CharField(blank=True, default=False, max_length=30, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('item', models.ManyToManyField(to='core.Item')),
            ],
            options={
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(default='5', max_length=3)),
                ('review', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('images', models.ManyToManyField(related_name='review_images', to='core.Multiple_Pics')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Paytm_order_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MERC_UNQ_REF', models.IntegerField(verbose_name='USER ID')),
                ('ORDERID', models.CharField(max_length=30, verbose_name='ORDER ID')),
                ('TXNDATE', models.DateTimeField(default=django.utils.timezone.now, verbose_name='TXN DATE')),
                ('TXNID', models.CharField(max_length=100, verbose_name='TXN ID')),
                ('BANKTXNID', models.CharField(blank=True, max_length=100, null=True, verbose_name='BANK TXN ID')),
                ('BANKNAME', models.CharField(blank=True, max_length=50, null=True, verbose_name='BANK NAME')),
                ('RESPCODE', models.IntegerField(verbose_name='RESP CODE')),
                ('PAYMENTMODE', models.CharField(blank=True, max_length=10, null=True, verbose_name='PAYMENT MODE')),
                ('CURRENCY', models.CharField(blank=True, max_length=4, null=True, verbose_name='CURRENCY')),
                ('GATEWAYNAME', models.CharField(blank=True, max_length=30, null=True, verbose_name='GATEWAY NAME')),
                ('MID', models.CharField(max_length=40)),
                ('RESPMSG', models.TextField(max_length=250, verbose_name='RESP MSG')),
                ('TXNAMOUNT', models.FloatField(verbose_name='TXN AMOUNT')),
                ('STATUS', models.CharField(max_length=12, verbose_name='STATUS')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_payment_order_paytm', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paytm_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MERC_UNQ_REF', models.IntegerField(verbose_name='USER ID')),
                ('ORDERID', models.CharField(max_length=30, verbose_name='ORDER ID')),
                ('TXNDATE', models.DateTimeField(default=django.utils.timezone.now, verbose_name='TXN DATE')),
                ('TXNID', models.CharField(max_length=100, verbose_name='TXN ID')),
                ('BANKTXNID', models.CharField(blank=True, max_length=100, null=True, verbose_name='BANK TXN ID')),
                ('BANKNAME', models.CharField(blank=True, max_length=50, null=True, verbose_name='BANK NAME')),
                ('RESPCODE', models.IntegerField(verbose_name='RESP CODE')),
                ('PAYMENTMODE', models.CharField(blank=True, max_length=10, null=True, verbose_name='PAYMENT MODE')),
                ('CURRENCY', models.CharField(blank=True, max_length=4, null=True, verbose_name='CURRENCY')),
                ('GATEWAYNAME', models.CharField(blank=True, max_length=30, null=True, verbose_name='GATEWAY NAME')),
                ('MID', models.CharField(max_length=40)),
                ('RESPMSG', models.TextField(max_length=250, verbose_name='RESP MSG')),
                ('TXNAMOUNT', models.FloatField(verbose_name='TXN AMOUNT')),
                ('STATUS', models.CharField(max_length=12, verbose_name='STATUS')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_payment_paytm', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('size', models.CharField(blank=True, default=False, max_length=25, null=True)),
                ('mrp_price', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('price_inc_ship', models.FloatField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
                ('referer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referer', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='core.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='core.Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images/')),
                ('description', models.CharField(max_length=500)),
                ('type', models.CharField(choices=[('A', 'All'), ('S', 'Specific')], max_length=3)),
                ('buttons', models.ManyToManyField(related_name='Redirectors', to='core.Clickables')),
                ('users', models.ManyToManyField(blank=True, related_name='Subscribers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Myorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myordered_date', models.DateField()),
                ('mydelivery_date', models.DateField()),
                ('status', models.CharField(choices=[('R', 'Refund'), ('S', 'Shipped'), ('P', 'Order Packed'), ('D', 'Out For Delivery'), ('O', 'Order Placed')], default='O', max_length=3)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
                ('orderitem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.OrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Itemdealer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pincode', models.CharField(max_length=30)),
                ('additional', models.CharField(max_length=100)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='keys',
            field=models.ManyToManyField(to='core.Keyword'),
        ),
        migrations.AddField(
            model_name='item',
            name='pics',
            field=models.ManyToManyField(blank=True, to='core.Multiple_Pics'),
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Sizes_class'),
        ),
        migrations.CreateModel(
            name='Extrasales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_name', models.CharField(max_length=30)),
                ('caption', models.CharField(blank=True, default=False, max_length=30, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('item', models.ManyToManyField(to='core.Item')),
            ],
            options={
                'verbose_name_plural': 'XtraSales',
            },
        ),
        migrations.CreateModel(
            name='ClubJoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refer', models.CharField(default=False, max_length=20)),
                ('usermoney', models.FloatField(default=0.0)),
                ('childern', models.IntegerField(default=0)),
                ('premium', models.BooleanField(default=False)),
                ('level', models.FloatField(default=1.0)),
                ('desig', models.CharField(choices=[('ManagingCaption', 'ManagingCaption'), ('SubordianteCaption', 'SubordianteCaption'), ('BronzeCaption', 'BronzeCaption'), ('SilverCaption', 'SilverCaption'), ('GoldCaption', 'GoldCaption'), ('Beginner', 'Beginner')], default='Beginner', max_length=20)),
                ('referincome', models.FloatField(default=0.0)),
                ('prod_ref_inc', models.FloatField(default=0.0)),
                ('orderincome', models.FloatField(default=0.0)),
                ('travelfund', models.FloatField(default=0.0)),
                ('teamincome', models.FloatField(default=0.0)),
                ('downlineincome', models.FloatField(default=0.0)),
                ('levelincome', models.FloatField(default=0.0)),
                ('positionincome', models.FloatField(default=0.0)),
                ('bonusincome', models.FloatField(default=0.0)),
                ('team', models.CharField(blank=True, default=False, max_length=30, null=True)),
                ('Acno', models.CharField(blank=True, default=False, max_length=30, null=True)),
                ('Ifsc', models.CharField(blank=True, default=False, max_length=30, null=True)),
                ('paytm', models.CharField(blank=True, default=False, max_length=30, null=True)),
                ('fund_transfered', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('referer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referer', to='core.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile')),
            ],
        ),
    ]
