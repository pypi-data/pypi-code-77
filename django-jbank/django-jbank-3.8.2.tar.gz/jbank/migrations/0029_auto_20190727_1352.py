# Generated by Django 2.2.3 on 2019-07-27 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jbank", "0028_auto_20190327_1830"),
    ]

    operations = [
        migrations.CreateModel(
            name="CurrencyExchange",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("record_date", models.DateField(db_index=True, verbose_name="record date")),
                ("source_currency", models.CharField(blank=True, max_length=3, verbose_name="source currency")),
                ("target_currency", models.CharField(blank=True, max_length=3, verbose_name="target currency")),
                ("unit_currency", models.CharField(blank=True, max_length=3, verbose_name="unit currency")),
                (
                    "exchange_rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=None,
                        max_digits=10,
                        null=True,
                        verbose_name="exchange rate",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StatementRecordDetail",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "batch_identifier",
                    models.CharField(
                        blank=True, db_index=True, default="", max_length=64, verbose_name="batch message id"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True,
                        db_index=True,
                        decimal_places=2,
                        default=None,
                        max_digits=10,
                        null=True,
                        verbose_name="amount",
                    ),
                ),
                ("currency_code", models.CharField(max_length=3, verbose_name="currency code")),
                (
                    "instructed_amount",
                    models.DecimalField(
                        blank=True,
                        db_index=True,
                        decimal_places=2,
                        default=None,
                        max_digits=10,
                        null=True,
                        verbose_name="instructed amount",
                    ),
                ),
                ("archive_identifier", models.CharField(blank=True, max_length=64, verbose_name="archive identifier")),
                (
                    "end_to_end_identifier",
                    models.CharField(blank=True, max_length=64, verbose_name="end-to-end identifier"),
                ),
                ("creditor_name", models.CharField(blank=True, max_length=128, verbose_name="creditor name")),
                ("creditor_account", models.CharField(blank=True, max_length=35, verbose_name="creditor account")),
                ("debtor_name", models.CharField(blank=True, max_length=128, verbose_name="debtor name")),
                (
                    "ultimate_debtor_name",
                    models.CharField(blank=True, max_length=128, verbose_name="ultimate debtor name"),
                ),
                (
                    "unstructured_remittance_info",
                    models.CharField(blank=True, max_length=128, verbose_name="unstructured remittance info"),
                ),
                (
                    "paid_date",
                    models.DateTimeField(blank=True, db_index=True, default=None, null=True, verbose_name="paid date"),
                ),
                (
                    "exchange",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="recorddetail_set",
                        to="jbank.CurrencyExchange",
                        verbose_name="currency exchange",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="statement",
            name="statement_identifier",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=48, verbose_name="statement identifier"
            ),
        ),
        migrations.AddField(
            model_name="statementrecord",
            name="family_code",
            field=models.CharField(blank=True, db_index=True, default="", max_length=4, verbose_name="family code"),
        ),
        migrations.AddField(
            model_name="statementrecord",
            name="record_domain",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PMNT", "Money Transfer (In/Out)"),
                    ("LDAS", "Loan Payment (Out)"),
                    ("CAMT", "Cash Management"),
                    ("ACMT", "Account Management"),
                    ("XTND", "Entended Domain"),
                    ("SECU", "Securities"),
                    ("FORX", "Foreign Exchange"),
                    ("XTND", "Entended Domain"),
                    ("NTAV", "Not Available"),
                ],
                db_index=True,
                max_length=4,
                verbose_name="record domain",
            ),
        ),
        migrations.AddField(
            model_name="statementrecord",
            name="sub_family_code",
            field=models.CharField(blank=True, db_index=True, default="", max_length=4, verbose_name="sub family code"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="bank_specific_info_1",
            field=models.CharField(blank=True, default="", max_length=1024, verbose_name="bank specific info (1)"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="contact_info_1",
            field=models.CharField(blank=True, default="", max_length=64, verbose_name="contact info (1)"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="customer_identifier",
            field=models.CharField(blank=True, default="", max_length=64, verbose_name="customer identifier"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="statement_number",
            field=models.SmallIntegerField(db_index=True, verbose_name="statement number"),
        ),
        migrations.AlterField(
            model_name="statementrecord",
            name="archive_identifier",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=64, verbose_name="archive identifier"
            ),
        ),
        migrations.AlterField(
            model_name="statementrecord",
            name="line_number",
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name="line number"),
        ),
        migrations.AlterField(
            model_name="statementrecord",
            name="record_code",
            field=models.CharField(
                choices=[
                    ("700", "Money Transfer (In/Out)"),
                    ("701", "Recurring Payment (In/Out)"),
                    ("702", "Bill Payment (Out)"),
                    ("703", "Payment Terminal Deposit (In)"),
                    ("704", "Bank Draft (In/Out)"),
                    ("705", "Reference Payments (In)"),
                    ("706", "Payment Service (Out)"),
                    ("710", "Deposit (In)"),
                    ("720", "Withdrawal (Out)"),
                    ("721", "Card Payment (Out)"),
                    ("722", "Check (Out)"),
                    ("730", "Bank Fees (Out)"),
                    ("740", "Interests Charged (Out)"),
                    ("750", "Interests Credited (In)"),
                    ("760", "Loan (Out)"),
                    ("761", "Loan Payment (Out)"),
                    ("770", "Foreign Transfer (In/Out)"),
                    ("780", "Zero Balancing (In/Out)"),
                    ("781", "Sweeping (In/Out)"),
                    ("782", "Topping (In/Out)"),
                ],
                db_index=True,
                max_length=4,
                verbose_name="record type",
            ),
        ),
        migrations.AlterField(
            model_name="statementrecord",
            name="record_description",
            field=models.CharField(blank=True, default="", max_length=128, verbose_name="record description"),
        ),
        migrations.AlterField(
            model_name="statementrecord",
            name="record_number",
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name="record number"),
        ),
        migrations.AlterField(
            model_name="statementrecord",
            name="remittance_info",
            field=models.CharField(blank=True, db_index=True, max_length=35, verbose_name="remittance info"),
        ),
        migrations.AlterField(
            model_name="statementrecordsepainfo",
            name="archive_identifier",
            field=models.CharField(blank=True, max_length=64, verbose_name="archive identifier"),
        ),
        migrations.CreateModel(
            name="StatementRecordRemittanceInfo",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "additional_info",
                    models.CharField(
                        blank=True, db_index=True, max_length=64, verbose_name="additional remittance info"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name="amount"
                    ),
                ),
                ("currency_code", models.CharField(blank=True, max_length=3, verbose_name="currency code")),
                ("reference", models.CharField(blank=True, db_index=True, max_length=35, verbose_name="reference")),
                (
                    "detail",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="remittanceinfo_set",
                        to="jbank.StatementRecordDetail",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="statementrecorddetail",
            name="record",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detail_set",
                to="jbank.StatementRecord",
                verbose_name="record",
            ),
        ),
    ]
