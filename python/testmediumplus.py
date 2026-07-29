async def test_id_token_missing_sub_claim_does_not_stamp(self, db, token_client):
        # Valid JWT but no ``sub`` claim → decode returns None → no stamp.
        vau = _vau()
        id_token_no_sub = jwt.encode({"iss": "test"}, "secret", algorithm="HS256")
        token_client.perform_vau_login = AsyncMock(return_value=_vau_response(id_token=id_token_no_sub))
        with patch("app.services.vau.identity.VAUInstanceRepository") as MockRepo:
            MockRepo.return_value.get_by_id = AsyncMock(return_value=vau)

            resolver = VAUOBOResolver(db, token_client)
            ctx = _ctx(
                **{
                    "x-opal-instance-id": "inst-1",
                    "x-opal-user-id": "vau-optiid-1",
                    "x-opal-vau-id": "vau-1",
                }
            )
