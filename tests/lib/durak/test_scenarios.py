from lib.durak import pass_with_many, yield_attack


def test_pass_with_last_card():
    assert pass_with_many(
        from_state={
            "hands": {
                "anna": ["10H"],
                "igor": ["9S", "QC"],
                "vasyl": ["AH", "10C"],
                "grusha": ["QS", None, "KH"],
            },
            "table": [["10D"]],
            "players": ["grusha", "anna", "vasyl", "igor"],
            "yielded": [],
            "draw_pile": [],
            "pass_count": 0,
            "trump_suit": "hearts",
            "lowest_rank": "6",
            "attack_limit": 6,
            "with_passing": True,
        },
        user="anna",
        payload={"cards": ["10H"]},
    ) == {
        "durak": None,
        "hands": {
            "anna": [None],
            "igor": ["9S", "QC"],
            "vasyl": ["AH", "10C"],
            "grusha": ["QS", None, "KH"],
        },
        "table": [["10D"], ["10H"]],
        "players": ["anna", "vasyl", "igor", "grusha"],
        "winners": set(["anna"]),
        "yielded": [],
        "defender": "vasyl",
        "attackers": ["igor", "grusha"],
        "draw_pile": [],
        "pass_count": 1,
        "trump_suit": "hearts",
        "lowest_rank": "6",
        "attack_limit": 6,
        "legal_passes": {"cards": set(["10C"]), "limit": 0},
        "with_passing": True,
        "legal_attacks": {"cards": set(), "limit": 0},
        "legal_defenses": {"10D": set(["AH"]), "10H": set(["AH"])},
    }


def test_defend_successfully_after_attack_plays_last_card():
    assert yield_attack(
        from_state={
            "hands": {
                "anna": ["KS", None, None, None, "JD", None],
                "igor": ["9S", "QD", None, "6S", "6D", "JS"],
                "vasyl": ["JC", "QS", "8C", "QH", None, "6H"],
                "grusha": [None, None],
            },
            "table": [["8H", "AH"], ["8D", "AD"], ["AC", "7S"], ["8S", "AS"]],
            "players": ["grusha", "anna", "vasyl", "igor"],
            "yielded": ["vasyl"],
            "draw_pile": [],
            "pass_count": 0,
            "trump_suit": "spades",
            "lowest_rank": "6",
            "attack_limit": 6,
            "with_passing": True,
        },
        user="igor",
        payload={},
    ) == {
        "durak": None,
        "hands": {
            "anna": ["KS", "JD"],
            "igor": ["9S", "QD", "6S", "6D", "JS"],
            "vasyl": ["JC", "QS", "8C", "QH", "6H"],
            "grusha": [],
        },
        "table": [],
        "players": ["anna", "vasyl", "igor", "grusha"],
        "winners": set(["grusha"]),
        "yielded": [],
        "defender": "vasyl",
        "attackers": ["anna"],
        "draw_pile": [],
        "pass_count": 0,
        "trump_suit": "spades",
        "lowest_rank": "6",
        "attack_limit": 6,
        "legal_passes": {"cards": set([]), "limit": 5},
        "with_passing": True,
        "legal_attacks": {"cards": set(["KS", "JD"]), "limit": 5},
        "legal_defenses": {},
    }
