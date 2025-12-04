from jsonparse.parser import Parser
import pytest

class TestParserComplexJSON:

    @pytest.fixture
    def parser(self):

        return Parser(stack_trace=False, queue_trace=False)

    @pytest.fixture
    def complex_json(self):
        return [
            {
                "id": "0001",
                "type": "donut",
                "exists": True,
                "ppu": 0.55,
                "batters": {
                    "batter": [
                        {"id": "1001", "type": "Reg"},
                        {"id": "1002", "type": "Chocolate"},
                        {"id": "1003", "type": "Blueberry"},
                        {"id": "1004", "type": "Devil's Food"},
                        {"start": 5, "end": 8}
                    ]
                },
                "topping": [
                    {"id": "5001", "ty": "None"},
                    {"id": "5002", "type": "Glazed"},
                    {"id": "5003", "type": "Sugar"},
                    {"id": "5004", "type": "Powdered Sugar"},
                    {"id": "5005", "type": "Chocolate with Sprinkles"},
                    {"id": "5006", "type": "Chocolate"},
                    {"id": "5007", "type": "Maple"}
                ],
                "start": 22,
                "end": 99
            },
            {
                "id": "0002",
                "type": "donut",
                "exists": False,
                "ppu": 42,
                "batters": {
                    "batter": [{"id": "1001", "type": "Rul"}]
                },
                "top_stuff": [
                    {"id": "5001", "typ": "None"},
                    {"id": "5002", "type": "Glazed"},
                    {"id": "5003", "type": "Sugar"},
                    {"id": "5004", "type": "Chocolate"},
                    {"id": "5005", "type": "Maple"}
                ],
                "start": 1,
                "end": 9
            },
            {
                "id": "0003",
                "type": "donut",
                "exists": None,
                "ppu": 7,
                "batters": {
                    "batter": [
                        {"id": "1001", "type": "Lar"},
                        {"id": "1002", "type": "Chocolate"}
                    ]
                },
                "on_top_thing": [
                    {"id": "5001", "type": "None"},
                    {"id": "5002", "type": "Glazed"},
                    {"id": "5003", "type": "Chocolate"},
                    {"id": "5004", "type": "Maple"}
                ],
                "start": 4,
                "end": 7
            }
        ]


    def test_find_key_id(self, parser, complex_json):
        """Find all 'id' keys."""
        result = parser.find_key(complex_json, "id", partial=False, case_sensitive=True)
        assert result == [
            '1001', '1002', '1003', '1004', '5001', '5002', '5003',
            '5004', '5005', '5006', '5007', '0001', '1001', '5001',
            '5002', '5003', '5004', '5005', '0002', '1001', '1002',
            '5001', '5002', '5003', '5004', '0003'
        ]

    def test_find_key_type(self, parser, complex_json):
        """Find all 'type' keys."""
        result = parser.find_key(complex_json, "type", partial=False, case_sensitive=True)
        print(result)
        assert result == [
            'Reg', 'Chocolate', 'Blueberry', "Devil's Food", 'Glazed', 'Sugar', 'Powdered Sugar', 
            'Chocolate with Sprinkles', 'Chocolate', 'Maple', 'donut', 'Rul', 'Glazed', 'Sugar', 
            'Chocolate', 'Maple', 'donut', 'Lar', 'Chocolate', 'None', 'Glazed', 'Chocolate', 'Maple', 'donut'
        ]

    def test_find_key_start(self, parser, complex_json):
        """Find all 'start' keys."""
        result = parser.find_key(complex_json, "start", partial=False, case_sensitive=True)
        assert result == [5, 22, 1, 4]

    def test_find_key_partial(self, parser, complex_json):
        """Find keys with partial match 'ty' (should match 'type' and 'typ' and 'ty')."""
        result = parser.find_key(complex_json, "ty", partial=True, case_sensitive=True)
        assert result == [
            'Reg', 'Chocolate', 'Blueberry', "Devil's Food", 'None', 'Glazed', 'Sugar', 'Powdered Sugar',
            'Chocolate with Sprinkles', 'Chocolate', 'Maple', 'donut', 'Rul', 'None', 'Glazed',
            'Sugar', 'Chocolate', 'Maple', 'donut', 'Lar', 'Chocolate', 'None',
            'Glazed', 'Chocolate', 'Maple', 'donut'
        ]

    def test_find_key_case_insensitive(self, parser, complex_json):
        """Find keys case-insensitively."""
        result = parser.find_key(complex_json, "TYPE", partial=False, case_sensitive=False)
        assert all(isinstance(x,str) for x in result)
        assert len(result)>10

    def test_find_key_nonexistent(self, parser, complex_json):
        """Try to find a non-existent key."""
        result = parser.find_key(complex_json, "unknown_key", partial=False, case_sensitive=True)
        assert result == []

    def test_invalid_data_type(self, parser, complex_json):
        """Pass invalid data type."""
        try:
            parser.find_key("invalid_data", "id", partial=False, case_sensitive=True)
        except TypeError:
            assert True

    def test_invalid_key_type(self, parser, complex_json):
        """Pass non-string key."""
        try:
            parser.find_key(complex_json, 1234, partial=False, case_sensitive=True)
        except TypeError:
            assert True

    def test_empty_key(self, parser, complex_json):
        """Pass empty key."""
        try:
            parser.find_key(complex_json, "", partial=False, case_sensitive=True)
        except ValueError:
            assert True
