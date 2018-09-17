from __future__ import absolute_import, unicode_literals

from django.utils.safestring import mark_safe

from wagtail.wagtailcore import blocks

from v1.blocks import AbstractFormBlock


class ConferenceRegistrationForm(AbstractFormBlock):
    govdelivery_code = blocks.CharBlock(
        label='GovDelivery code',
        help_text=(
            'Conference registrants will be subscribed to this GovDelivery '
            'topic.'
        )
    )
    govdelivery_question_id = blocks.RegexBlock(
        required=False,
        regex=r'^\d{5,}$',
        error_messages={
            'invalid': 'GovDelivery question ID must be 5 digits.'
        },
        label='GovDelivery question ID',
        help_text=mark_safe(
            'Enter the ID of the question in GovDelivery that is being used '
            'to track registration for this conference. It is the number in '
            'the question URL, e.g., the <code>12345</code> in '
            '<code>https://admin.govdelivery.com/questions/12345/edit</code>.'
        )
    )
    govdelivery_answer_id = blocks.RegexBlock(
        required=False,
        regex=r'^\d{5,}$',
        error_messages={
            'invalid': 'GovDelivery answer ID must be 5 digits.'
        },
        label='GovDelivery answer ID',
        help_text=mark_safe(
            'Enter the ID of the affrimative answer for the above question. '
            'To find it, right-click on the answer in the listing on a page '
            'like <code>https://admin.govdelivery.com/questions/12345/answers'
            '</code>, inspect the element, and look around in the source for '
            'a five-digit ID associated with that answer. <strong>Required '
            'if Govdelivery question ID is set.</strong>'
        )
    )
    capacity = blocks.IntegerBlock(
        help_text=(
            'Enter the (physical) conference attendance limit as a number.'
        )
    )
    success_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown on successful registration.'
        )
    )
    at_capacity_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown when the event is at capacity.'
        )
    )
    failure_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown if the GovDelivery '
            'subscription fails.'
        )
    )

    class Meta:
        handler = 'data_research.handlers.ConferenceRegistrationHandler'
        template = 'data_research/conference-registration-form.html'

    # Custom clean to check for both question ID and answer ID


class MortgageDataDownloads(blocks.StructBlock):
    show_archives = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text=(
            'Check this box to allow the archival section to display. '
            'No section will appear if there are no archival downloads.'))

    class Meta:
        label = 'Mortgage Downloads Block'
        icon = 'table'
        template = '_includes/organisms/mortgage-performance-downloads.html'
