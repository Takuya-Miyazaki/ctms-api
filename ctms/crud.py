from typing import Dict, List, Optional

from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session

from .models import AmoAccount, Email, FirefoxAccount, Newsletter, VpnWaitlist
from .schemas import (
    AddOnsSchema,
    ContactInSchema,
    ContactSchema,
    EmailInSchema,
    EmailSchema,
    FirefoxAccountsSchema,
    NewsletterSchema,
    VpnWaitlistSchema,
)


def get_email_by_email_id(db: Session, email_id: UUID4):
    return db.query(Email).filter(Email.email_id == email_id).first()


def get_contact_by_email_id(db: Session, email_id: UUID4):
    """Get all the data for a contact."""
    result = (
        db.query(Email, AmoAccount, FirefoxAccount, VpnWaitlist)
        .outerjoin(AmoAccount, Email.email_id == AmoAccount.email_id)
        .outerjoin(FirefoxAccount, Email.email_id == FirefoxAccount.email_id)
        .outerjoin(VpnWaitlist, Email.email_id == VpnWaitlist.email_id)
        .filter(Email.email_id == email_id)
        .first()
    )
    if result is None:
        return None
    email, amo, fxa, vpn_waitlist = result
    newsletters = db.query(Newsletter).filter(Newsletter.email_id == email_id).all()
    return {
        "amo": amo,
        "email": email,
        "fxa": fxa,
        "newsletters": newsletters,
        "vpn_waitlist": vpn_waitlist,
    }


def get_contacts_by_any_id(
    db: Session,
    email_id: Optional[UUID4] = None,
    primary_email: Optional[EmailStr] = None,
    basket_token: Optional[UUID4] = None,
    sfdc_id: Optional[str] = None,
    mofo_id: Optional[str] = None,
    amo_user_id: Optional[str] = None,
    fxa_id: Optional[str] = None,
    fxa_primary_email: Optional[EmailStr] = None,
) -> List[Dict]:
    """Get all the data for multiple contacts by IDs."""
    assert any(
        (
            email_id,
            primary_email,
            basket_token,
            sfdc_id,
            mofo_id,
            amo_user_id,
            fxa_id,
            fxa_primary_email,
        )
    )
    statement = (
        db.query(Email, AmoAccount, FirefoxAccount, VpnWaitlist)
        .outerjoin(AmoAccount, Email.email_id == AmoAccount.email_id)
        .outerjoin(FirefoxAccount, Email.email_id == FirefoxAccount.email_id)
        .outerjoin(VpnWaitlist, Email.email_id == VpnWaitlist.email_id)
    )
    if email_id is not None:
        statement = statement.filter(Email.email_id == email_id)
    if primary_email is not None:
        statement = statement.filter(Email.primary_email == primary_email)
    if basket_token is not None:
        statement = statement.filter(Email.basket_token == str(basket_token))
    if sfdc_id is not None:
        statement = statement.filter(Email.sfdc_id == sfdc_id)
    if mofo_id is not None:
        statement = statement.filter(Email.mofo_id == mofo_id)
    if amo_user_id is not None:
        statement = statement.filter(AmoAccount.user_id == amo_user_id)
    if fxa_id is not None:
        statement = statement.filter(FirefoxAccount.fxa_id == fxa_id)
    if fxa_primary_email is not None:
        statement = statement.filter(FirefoxAccount.primary_email == fxa_primary_email)
    results = statement.all()
    data = []
    for result in results:
        email, amo, fxa, vpn_waitlist = result
        newsletters = (
            db.query(Newsletter).filter(Newsletter.email_id == email.email_id).all()
        )
        data.append(
            {
                "amo": amo,
                "email": email,
                "fxa": fxa,
                "newsletters": newsletters,
                "vpn_waitlist": vpn_waitlist,
            }
        )
    return data


def create_amo(db: Session, email_id: UUID4, amo: AddOnsSchema):
    db_amo = AmoAccount(email_id=email_id, **amo.dict())
    db.add(db_amo)


def create_email(db: Session, email: EmailInSchema):
    db_email = Email(**email.dict())
    db.add(db_email)


def create_fxa(db: Session, email_id: UUID4, fxa: FirefoxAccountsSchema):
    db_fxa = FirefoxAccount(email_id=email_id, **fxa.dict())
    db.add(db_fxa)


def create_vpn_waitlist(db: Session, email_id: UUID4, vpn_waitlist: VpnWaitlistSchema):
    db_vpn_waitlist = VpnWaitlist(email_id=email_id, **vpn_waitlist.dict())
    db.add(db_vpn_waitlist)


def create_newsletter(db: Session, email_id: UUID4, newsletter: NewsletterSchema):
    db_newsletter = Newsletter(email_id=email_id, **newsletter.dict())
    db.add(db_newsletter)


def create_contact(db: Session, email_id: UUID4, contact: ContactInSchema):
    create_email(db, contact.email)
    if contact.amo:
        create_amo(db, email_id, contact.amo)
    if contact.fxa:
        create_fxa(db, email_id, contact.fxa)
    if contact.vpn_waitlist:
        create_vpn_waitlist(db, email_id, contact.vpn_waitlist)
    for newsletter in contact.newsletters:
        create_newsletter(db, email_id, newsletter)
