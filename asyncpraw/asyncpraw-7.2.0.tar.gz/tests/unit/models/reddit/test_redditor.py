import pytest

from asyncpraw.models import Redditor

from ... import UnitTest


class TestRedditor(UnitTest):
    def test_equality(self):
        redditor1 = Redditor(self.reddit, _data={"name": "dummy1", "n": 1})
        redditor2 = Redditor(self.reddit, _data={"name": "Dummy1", "n": 2})
        redditor3 = Redditor(self.reddit, _data={"name": "dummy3", "n": 2})
        assert redditor1 == redditor1
        assert redditor2 == redditor2
        assert redditor3 == redditor3
        assert redditor1 == redditor2
        assert redditor2 != redditor3
        assert redditor1 != redditor3
        assert "dummy1" == redditor1
        assert redditor2 == "dummy1"

    def test_construct_failure(self):
        message = "Exactly one of `name`, `fullname`, or `_data` must be provided."
        with pytest.raises(TypeError) as excinfo:
            Redditor(self.reddit)
        assert str(excinfo.value) == message

        with pytest.raises(TypeError) as excinfo:
            Redditor(self.reddit, "dummy", _data={"id": "dummy"})
        assert str(excinfo.value) == message

        with pytest.raises(TypeError) as excinfo:
            Redditor(self.reddit, name="dummy", fullname="t2_dummy")
        assert str(excinfo.value) == message

        with pytest.raises(TypeError) as excinfo:
            Redditor(
                self.reddit,
                name="dummy",
                fullname="t2_dummy",
                _data={"id": "dummy"},
            )
        assert str(excinfo.value) == message

        with pytest.raises(AssertionError):
            Redditor(self.reddit, _data=[{"name": "dummy"}])

        with pytest.raises(AssertionError):
            Redditor(self.reddit, _data={"notname": "dummy"})

        with pytest.raises(ValueError):
            Redditor(self.reddit, "")
        with pytest.raises(ValueError):
            Redditor(self.reddit, fullname="")

    def test_fullname(self):
        redditor = Redditor(self.reddit, _data={"name": "name", "id": "dummy"})
        assert redditor.fullname == "t2_dummy"

    async def test_guild__min(self):
        with pytest.raises(TypeError) as excinfo:
            await Redditor(self.reddit, name="RedditorName").gild(0)
        assert str(excinfo.value) == "months must be between 1 and 36"

    async def test_guild__max(self):
        with pytest.raises(TypeError) as excinfo:
            await Redditor(self.reddit, name="RedditorName").gild(37)
        assert str(excinfo.value) == "months must be between 1 and 36"

    def test_hash(self):
        redditor1 = Redditor(self.reddit, _data={"name": "dummy1", "n": 1})
        redditor2 = Redditor(self.reddit, _data={"name": "Dummy1", "n": 2})
        redditor3 = Redditor(self.reddit, _data={"name": "dummy3", "n": 2})
        assert hash(redditor1) == hash(redditor1)
        assert hash(redditor2) == hash(redditor2)
        assert hash(redditor3) == hash(redditor3)
        assert hash(redditor1) == hash(redditor2)
        assert hash(redditor2) != hash(redditor3)
        assert hash(redditor1) != hash(redditor3)

    def test_repr(self):
        redditor = Redditor(self.reddit, name="RedditorName")
        assert repr(redditor) == "Redditor(name='RedditorName')"

    def test_str(self):
        redditor = Redditor(self.reddit, _data={"name": "name", "id": "dummy"})
        assert str(redditor) == "name"


class TestRedditorListings(UnitTest):
    def test__params_not_modified_in_mixed_listing(self):
        params = {"dummy": "value"}
        redditor = Redditor(self.reddit, name="spez")
        for listing in ["controversial", "hot", "new", "top"]:
            generator = getattr(redditor, listing)(params=params)
            assert params == {"dummy": "value"}
            assert listing == generator.params["sort"]
            assert "value" == generator.params["dummy"]
