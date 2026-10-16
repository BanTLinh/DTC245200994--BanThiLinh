from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Tên loại hợp đồng')),
                ('description', models.TextField(blank=True, verbose_name='Mô tả')),
            ],
            options={
                'verbose_name': 'Loại hợp đồng',
                'verbose_name_plural': 'Danh mục Loại hợp đồng',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Tên đối tác')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Mã đối tác')),
                ('tax_code', models.CharField(blank=True, max_length=50, verbose_name='Mã số thuế')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Số điện thoại')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email liên hệ')),
                ('address', models.TextField(blank=True, verbose_name='Địa chỉ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
            ],
            options={
                'verbose_name': 'Đối tác',
                'verbose_name_plural': 'Danh sách Đối tác',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(max_length=100, unique=True, verbose_name='Số hợp đồng')),
                ('title', models.CharField(max_length=255, verbose_name='Tên hợp đồng')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Giá trị hợp đồng (VNĐ)')),
                ('sign_date', models.DateField(blank=True, null=True, verbose_name='Ngày ký kết')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Ngày hiệu lực')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Ngày hết hạn')),
                ('status', models.CharField(choices=[('DRAFT', 'Dự thảo'), ('PENDING', 'Chờ phê duyệt'), ('ACTIVE', 'Đang thực hiện'), ('COMPLETED', 'Đã thanh lý'), ('TERMINATED', 'Đã chấm dứt / Hủy')], default='DRAFT', max_length=20, verbose_name='Trạng thái')),
                ('note', models.TextField(blank=True, verbose_name='Ghi chú điều khoản')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')),
                ('contract_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contracts.contracttype', verbose_name='Loại hợp đồng')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='contracts.partner', verbose_name='Đối tác')),
            ],
            options={
                'verbose_name': 'Hợp đồng',
                'verbose_name_plural': 'Danh sách Hợp đồng',
                'ordering': ['-created_at'],
            },
        ),
    ]
