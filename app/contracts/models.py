from django.db import models

class Partner(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên đối tác")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã đối tác")
    tax_code = models.CharField(max_length=50, blank=True, verbose_name="Mã số thuế")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email liên hệ")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Đối tác"
        verbose_name_plural = "Danh sách Đối tác"
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class ContractType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên loại hợp đồng")
    description = models.TextField(blank=True, verbose_name="Mô tả")

    class Meta:
        verbose_name = "Loại hợp đồng"
        verbose_name_plural = "Danh mục Loại hợp đồng"

    def __str__(self):
        return self.name


class Contract(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Dự thảo'),
        ('PENDING', 'Chờ phê duyệt'),
        ('ACTIVE', 'Đang thực hiện'),
        ('COMPLETED', 'Đã thanh lý'),
        ('TERMINATED', 'Đã chấm dứt / Hủy'),
    ]

    contract_number = models.CharField(max_length=100, unique=True, verbose_name="Số hợp đồng")
    title = models.CharField(max_length=255, verbose_name="Tên hợp đồng")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='contracts', verbose_name="Đối tác")
    contract_type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Loại hợp đồng")
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Giá trị hợp đồng (VNĐ)")
    sign_date = models.DateField(null=True, blank=True, verbose_name="Ngày ký kết")
    start_date = models.DateField(null=True, blank=True, verbose_name="Ngày hiệu lực")
    end_date = models.DateField(null=True, blank=True, verbose_name="Ngày hết hạn")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT', verbose_name="Trạng thái")
    note = models.TextField(blank=True, verbose_name="Ghi chú điều khoản")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")

    class Meta:
        verbose_name = "Hợp đồng"
        verbose_name_plural = "Danh sách Hợp đồng"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contract_number} - {self.title}"
