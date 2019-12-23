import graphene
from ..domain.invoice import Invoice


class InvoiceMeta(graphene.ObjectType):
    id = graphene.Int()
    date = graphene.String()
    patient_id = graphene.Int()
    name = graphene.String()
    identifier = graphene.String()
    text = graphene.String()


class InvoicesMeta(graphene.ObjectType):
    total = graphene.Int()
    entry = graphene.List(InvoiceMeta)
    offset = graphene.Int()
    count = graphene.Int()


class InvoiceInput(graphene.InputObjectType):
    date = graphene.String()
    patient_id = graphene.Int()
    name = graphene.String()
    identifier = graphene.String()
    text = graphene.String()


class CreateInvoice(graphene.Mutation):
    class Arguments:
        invoice_data = InvoiceInput(required=True)

    ok = graphene.Boolean()
    invoice = graphene.Field(InvoiceMeta)

    @staticmethod
    def mutate(root, info, invoice_data):
        try:
            invoice = Invoice.create(**invoice_data)
            return CreateInvoice(invoice=invoice, ok=True)
        except Exception:
            return CreateInvoice(invoice=None, ok=False)
