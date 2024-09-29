import unittest
from pages.Stakeholder_Management import calculate_score  # Importiere die Funktion, die du testen möchtest

class TestCalculateScore(unittest.TestCase):
    def test_calculate_score_high_values(self):
        """Testet, ob der Score korrekt berechnet wird, wenn alle Werte hoch sind."""
        row = {
            'Level des Engagements': 'Hoch',
            'Kommunikation': 'Regelmäßig',
            'Zeithorizont': 'Langfristig',
            'Auswirkung auf Interessen': 'Hoch'
        }
        score = calculate_score(row)
        self.assertEqual(score, 100)  # Der maximale Score sollte 100 sein

    def test_calculate_score_low_values(self):
        """Testet, ob der Score korrekt berechnet wird, wenn alle Werte niedrig sind."""
        row = {
            'Level des Engagements': 'Niedrig',
            'Kommunikation': 'Nie',
            'Zeithorizont': 'Kurzfristig',
            'Auswirkung auf Interessen': 'Niedrig'
        }
        score = calculate_score(row)
        self.assertEqual(score, 0)  # Der minimale Score sollte 0 sein

    def test_calculate_score_mixed_values(self):
        """Testet, ob der Score korrekt berechnet wird, wenn die Werte gemischt sind."""
        row = {
            'Level des Engagements': 'Mittel',
            'Kommunikation': 'Gelegentlich',
            'Zeithorizont': 'Mittelfristig',
            'Auswirkung auf Interessen': 'Mittel'
        }
        score = calculate_score(row)
        self.assertEqual(score, 50)  # Bei gemischten Werten sollte der Score etwa 50 sein

if __name__ == '__main__':
    unittest.main()
