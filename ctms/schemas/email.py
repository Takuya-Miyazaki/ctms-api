from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID, uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field, HttpUrl

email_id_field: UUID4 = Field(
    description="ID for email",
    example="332de237-cab7-4461-bcc3-48e68f42bd5c",
)


class EmailBase(BaseModel):
    """Data that is included in input/output/db of a primary_email and such."""

    primary_email: EmailStr = Field(
        ...,
        description="Contact email address, Email in Salesforce",
        example="contact@example.com",
    )
    basket_token: Optional[UUID] = Field(
        ...,
        description="Basket token, Token__c in Salesforce",
        example="c4a7d759-bb52-457b-896b-90f1d3ef8433",
    )
    double_opt_in: bool = Field(
        default=False, description="User has clicked a confirmation link", example=True
    )
    sfdc_id: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Salesforce legacy ID, Id in Salesforce",
        example="001A000023aABcDEFG",
    )
    mofo_id: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Foriegn key to MoFo contact database",
    )
    first_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="First name of contact, FirstName in Salesforce",
        example="Jane",
    )
    last_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Last name of contact, LastName in Salesforce",
        example="Doe",
    )
    mailing_country: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Mailing country code, 2 lowercase letters, MailingCountryCode in Salesforce",
        example="us",
    )
    email_format: Literal["H", "T", "N", ""] = Field(
        default="H",
        description="Email format, H=HTML, T=Plain Text, N and Empty=No selection, Email_Format__c in Salesforce",
    )
    email_lang: Optional[str] = Field(
        default="en",
        max_length=5,
        description="Email language code, usually 2 lowercase letters, Email_Language__c in Salesforce",
    )
    mofo_relevant: bool = Field(
        default=False, description="Mozilla Foundation is tracking this email"
    )
    has_opted_out_of_email: bool = Field(
        default=False,
        description="User has opted-out, HasOptedOutOfEmail in Salesforce",
    )
    unsubscribe_reason: Optional[str] = Field(
        default=None,
        description="Reason for unsubscribing, in basket IGNORE_USER_FIELDS, Unsubscribe_Reason__c in Salesforce",
    )

    class Config:
        orm_mode = True


class EmailSchema(EmailBase):
    email_id: UUID4 = email_id_field
    create_timestamp: Optional[datetime] = Field(
        default=None,
        description="Contact creation date, CreatedDate in Salesforce",
        example="2020-03-28T15:41:00.000Z",
    )
    update_timestamp: Optional[datetime] = Field(
        default=None,
        description="Contact last modified date, LastModifiedDate in Salesforce",
        example="2021-01-28T21:26:57.511Z",
    )

    # TODO: Is overriding equality the best way
    #       to add this specific comparison or should
    #       we add it as a `.compare` or something?
    def __eq__(self, other):
        if not isinstance(other, EmailBase):
            return False

        # We exclude these fields because they are
        # generated server-side and not useful
        # for comparison in most cases. Check directly
        # that these fields are equivalent if you want
        # to do that
        excluded_in_comparison = {"create_timestamp", "update_timestamp"}

        return self.dict(exclude=excluded_in_comparison) == other.dict(
            exclude=excluded_in_comparison
        )


class EmailInSchema(EmailBase):
    email_id: Optional[UUID4] = email_id_field

    # TODO: Is overriding equality the best way
    #       to add this specific comparison or should
    #       we add it as a `.compare` or something?
    def __eq__(self, other):
        if not isinstance(other, EmailBase):
            return False
        if self.email_id is None or other.email_id is None:
            raise BaseException("Cannot compare Email instances without email_id")
        return super().__eq__(self, other)
