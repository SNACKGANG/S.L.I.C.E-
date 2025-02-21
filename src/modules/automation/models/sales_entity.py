class Sale:
    """
    Represents a sale transaction.
    """

    def __init__(
        self,
        name,
        token_id,
        contract,
        price_native,
        price_usd,
        timestamp,
        seller,
        buyer,
        image,
        collection_data,
        channel_ids=None,
    ):
        self.token_id = token_id
        self.name = name
        self.contract = contract
        self.price_native = price_native
        self.price_usd = price_usd
        self.timestamp = timestamp
        self.seller = seller
        self.buyer = buyer
        self.image = image
        self.collection_data = collection_data
        self.channel_ids = channel_ids if channel_ids else []
