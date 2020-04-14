from datetime import date, timedelta
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from prepaid_agreements.models import PrepaidAgreement, PrepaidProduct
from prepaid_agreements.scripts.write_prepaid_agreements_data_to_csv import (
    write_agreements_data
)


class TestViews(TestCase):

    def setUp(self):
        self.product1 = PrepaidProduct(
            issuer_name='Bank of CFPB',
            prepaid_type='Tax'
        )
        self.product1.save()
        self.product2 = PrepaidProduct(
            issuer_name='CFPB Bank',
            prepaid_type='Tax',
            other_relevant_parties='Party'
        )
        self.product2.save()

        effective_date = date(month=2, day=3, year=2019)
        self.agreement_old = PrepaidAgreement(
            effective_date=effective_date,
            created_time=timezone.now() - timedelta(hours=1),
            product=self.product1,
        )
        self.agreement_old.save()
        self.agreement_older = PrepaidAgreement(
            effective_date=effective_date,
            created_time=timezone.now() - timedelta(hours=2),
            product=self.product2,
        )
        self.agreement_older.save()
        self.agreement_new = PrepaidAgreement(
            effective_date=effective_date,
            created_time=timezone.now(),
            product=self.product1,
        )
        self.agreement_new.save()

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_write_agreements_data(self, mock_open):

        # Run the write function
        write_agreements_data()

        mock_file_handle = mock_open()

        # Make sure each file's headers exist
        mock_file_handle.write.assert_any_call(
            'issuer_name,product_name,product_id,'
            'agreement_effective_date,agreement_id,most_recent_agreement,'
            'created_date,current_status,withdrawal_date,'
            'prepaid_product_type,program_manager_exists,program_manager,'
            'other_relevant_parties,path,direct_download\r\n'
        )
        mock_file_handle.write.assert_any_call(
            'issuer_name,product_name,product_id,'
            'agreement_effective_date,agreement_id,'
            'created_date,current_status,withdrawal_date,'
            'prepaid_product_type,program_manager_exists,program_manager,'
            'other_relevant_parties,path,direct_download\r\n'
        )

        # Make sure expected data rows exist
        mock_file_handle.write.assert_any_call(
            'Bank of CFPB,,1,2019-02-03,1,No,2020-04-14 14:26:48,,,Tax,,,'
            'No information provided,,\r\n'
        )
        mock_file_handle.write.assert_any_call(
            'Bank of CFPB,,1,2019-02-03,3,2020-04-14 15:26:48,,,Tax,,,'
            'No information provided,,\r\n'
        )
        mock_file_handle.write.assert_any_call(
            'Bank of CFPB,,1,2019-02-03,3,Yes,2020-04-14 15:26:48,,,Tax,,,'
            'No information provided,,\r\n'
        )
        mock_file_handle.write.assert_any_call(
            'CFPB Bank,,2,2019-02-03,2,2020-04-14 13:26:48,,,Tax,,,'
            'Party,,\r\n'
        )
        mock_file_handle.write.assert_any_call(
            'CFPB Bank,,2,2019-02-03,2,Yes,2020-04-14 13:26:48,,,Tax,,,'
            'Party,,\r\n'
        )
