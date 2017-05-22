# -*- coding: utf-8 -*-
import unittest

from openprocurement.api.tests.base import snitch

from openprocurement.tender.esco.tests.base import (
    BaseESCOEUContentWebTest,
    test_bids,
    test_lots,
)
from openprocurement.tender.openeu.tests.qualification_blanks import (
    # Tender2LotQualificationClaimResourceTest
    create_tender_qualification_claim,
    # Tender2LotQualificationComplaintResourceTest
    create_tender_2lot_qualification_complaint,
    patch_tender_2lot_qualification_complaint,
    change_status_to_standstill_with_complaint_cancel_lot,
    # TenderLotQualificationComplaintResourceTest
    create_tender_lot_qualification_complaint,
    patch_tender_lot_qualification_complaint,
    get_tender_lot_qualification_complaint,
    get_tender_lot_qualification_complaints,
    # TenderQualificationComplaintResourceTest
    create_tender_qualification_complaint_invalid,
    create_tender_qualification_complaint,
    patch_tender_qualification_complaint,
    review_tender_qualification_complaint,
    review_tender_award_claim,
    get_tender_qualification_complaint,
    get_tender_qualification_complaints,
    change_status_to_standstill_with_complaint,
    # Tender2LotQualificationResourceTest
    lot_patch_tender_qualifications,
    lot_get_tender_qualifications_collection,
    tender_qualification_cancelled,
    # TenderQualificationResourceTest
    post_tender_qualifications,
    get_tender_qualifications_collection,
    patch_tender_qualifications,
    get_tender_qualifications,
    patch_tender_qualifications_after_status_change
)


class TenderQualificationResourceTest(BaseESCOEUContentWebTest):
    initial_status = 'active.tendering'  # 'active.pre-qualification' status sets in setUp
    initial_bids = test_bids
    initial_auth = ('Basic', ('broker', ''))

    def setUp(self):
        super(TenderQualificationResourceTest, self).setUp()

        # update periods to have possibility to change tender status by chronograph
        self.set_status("active.pre-qualification", extra={'status': 'active.tendering'})

        # simulate chronograph tick
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/tenders/{}'.format(self.tender_id), {"data": {"id": self.tender_id}})
        self.assertEqual(response.json['data']['status'], 'active.pre-qualification')
        self.app.authorization = auth

    test_post_tender_qualifications = snitch(post_tender_qualifications)
    test_get_tender_qualifications_collection = snitch(get_tender_qualifications_collection)
    test_patch_tender_qualifications = snitch(patch_tender_qualifications)
    test_get_tender_qualifications = snitch(get_tender_qualifications)
    test_patch_tender_qualifications_after_status_change = snitch(patch_tender_qualifications_after_status_change)


class Tender2LotQualificationResourceTest(TenderQualificationResourceTest):
    initial_status = 'active.tendering'  # 'active.pre-qualification.stand-still' status sets in setUp
    initial_lots = 2 * test_lots
    initial_bids = test_bids
    initial_auth = ('Basic', ('broker', ''))

    def setUp(self):
        super(TenderQualificationResourceTest, self).setUp()

        # update periods to have possibility to change tender status by chronograph
        self.set_status("active.pre-qualification", extra={'status': 'active.tendering'})

        # simulate chronograph tick
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/tenders/{}'.format(self.tender_id), {"data": {"id": self.tender_id}})
        self.assertEqual(response.json['data']['status'], 'active.pre-qualification')
        self.app.authorization = auth

        response = self.app.get('/tenders/{}/qualifications'.format(self.tender_id))
        self.assertEqual(response.content_type, 'application/json')
        qualifications = response.json['data']

    test_patch_tender_qualifications = snitch(lot_patch_tender_qualifications)
    test_get_tender_qualifications_collection = snitch(lot_get_tender_qualifications_collection)
    test_tender_qualification_cancelled = snitch(tender_qualification_cancelled)


class TenderQualificationComplaintResourceTest(BaseESCOEUContentWebTest):
    initial_status = 'active.tendering'  # 'active.pre-qualification.stand-still' status sets in setUp
    initial_bids = test_bids
    initial_auth = ('Basic', ('broker', ''))

    def setUp(self):
        super(TenderQualificationComplaintResourceTest, self).setUp()

        # update periods to have possibility to change tender status by chronograph
        self.set_status("active.pre-qualification", extra={'status': 'active.tendering'})

        # simulate chronograph tick
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/tenders/{}'.format(self.tender_id), {"data": {"id": self.tender_id}})
        self.assertEqual(response.json['data']['status'], 'active.pre-qualification')
        self.app.authorization = auth

        response = self.app.get('/tenders/{}/qualifications'.format(self.tender_id))
        self.assertEqual(response.content_type, 'application/json')
        qualifications = response.json['data']
        self.qualification_id = qualifications[0]['id']

        for qualification in qualifications:
            response = self.app.patch_json('/tenders/{}/qualifications/{}?acc_token={}'.format(self.tender_id, qualification['id'], self.tender_token),
                                           {"data": {"status": "active", "qualified": True, "eligible": True}})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['status'], 'active')

        response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token),
                                       {"data": {"status": "active.pre-qualification.stand-still"}})
        self.assertEqual(response.status, '200 OK')

    test_create_tender_qualification_complaint_invalid = snitch(create_tender_qualification_complaint_invalid)
    test_create_tender_qualification_complaint = snitch(create_tender_qualification_complaint)
    test_patch_tender_qualification_complaint = snitch(patch_tender_qualification_complaint)
    test_review_tender_qualification_complaint = snitch(review_tender_qualification_complaint)
    test_review_tender_award_claim = snitch(review_tender_award_claim)
    test_get_tender_qualification_complaint = snitch(get_tender_qualification_complaint)
    test_get_tender_qualification_complaints = snitch(get_tender_qualification_complaints)
    test_change_status_to_standstill_with_complaint = snitch(change_status_to_standstill_with_complaint)


class TenderLotQualificationComplaintResourceTest(TenderQualificationComplaintResourceTest):
    initial_lots = test_lots

    initial_auth = ('Basic', ('broker', ''))

    test_create_tender_qualification_complaint = snitch(create_tender_lot_qualification_complaint)
    test_patch_tender_qualification_complaint = snitch(patch_tender_lot_qualification_complaint)
    test_get_tender_qualification_complaint = snitch(get_tender_lot_qualification_complaint)
    test_get_tender_qualification_complaints = snitch(get_tender_lot_qualification_complaints)


class Tender2LotQualificationComplaintResourceTest(TenderLotQualificationComplaintResourceTest):
    initial_lots = 2 * test_lots

    initial_auth = ('Basic', ('broker', ''))
    after_qualification_switch_to = "active.auction"

    test_create_tender_qualification_complaint = snitch(create_tender_2lot_qualification_complaint)
    test_patch_tender_qualification_complaint = snitch(patch_tender_2lot_qualification_complaint)
    test_change_status_to_standstill_with_complaint_cancel_lot = snitch(change_status_to_standstill_with_complaint_cancel_lot)


class Tender2LotQualificationClaimResourceTest(Tender2LotQualificationComplaintResourceTest):

    after_qualification_switch_to = "unsuccessful"

    def setUp(self):
        super(TenderQualificationComplaintResourceTest, self).setUp()

        # update periods to have possibility to change tender status by chronograph
        self.set_status("active.pre-qualification", extra={'status': 'active.tendering'})

        # simulate chronograph tick
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/tenders/{}'.format(self.tender_id), {"data": {"id": self.tender_id}})
        self.assertEqual(response.json['data']['status'], 'active.pre-qualification')
        self.app.authorization = auth

        response = self.app.get('/tenders/{}/qualifications'.format(self.tender_id))
        self.assertEqual(response.content_type, 'application/json')
        qualifications = response.json['data']
        self.qualification_id = qualifications[0]['id']

        for qualification in qualifications:
            if qualification['bidID'] == self.initial_bids[0]['id']:
                response = self.app.patch_json('/tenders/{}/qualifications/{}?acc_token={}'.format(self.tender_id, qualification['id'], self.tender_token),
                                               {"data": {"status": "active", "qualified": True, "eligible": True}})
                self.assertEqual(response.status, '200 OK')
                self.assertEqual(response.json['data']['status'], 'active')
            else:
                response = self.app.patch_json('/tenders/{}/qualifications/{}?acc_token={}'.format(self.tender_id, qualification['id'], self.tender_token),
                                               {"data": {"status": "unsuccessful"}})
                self.assertEqual(response.status, '200 OK')
                self.assertEqual(response.json['data']['status'], 'unsuccessful')
                self.unsuccessful_qualification_id = qualification['id']

        response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token),
                                       {"data": {"status": "active.pre-qualification.stand-still"}})
        self.assertEqual(response.status, '200 OK')

    test_create_tender_qualification_claim = snitch(create_tender_qualification_claim)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderQualificationResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')