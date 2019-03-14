
class CertificationRequest(models.Model):
    software_statement = fields.JSONField()
    public_key = fields.TextField()
    private_key = fields.TextField() # keep hidden?
    signature = fields.TextField(null=True)
    created = fields.DateTime()

    def sign(self):
        pass
