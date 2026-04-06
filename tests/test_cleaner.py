from src.utils.cleaner import normalize_tags, extract_salary_parts

def test_normalize_tags():
    assert normalize_tags("python,  javascript , react") == "python, javascript, react"
    assert normalize_tags("") == "not mentioned"
    assert normalize_tags(None) == "not mentioned"

def test_extract_salary_parts_numeric():
    s_from, s_to, curr = extract_salary_parts("$100k - $150k")
    assert s_from == 100000
    assert s_to == 150000
    assert curr == "$"

def test_extract_salary_parts_euro():
    s_from, s_to, curr = extract_salary_parts("€80,000")
    assert s_from == 80000
    assert s_to == 80000
    assert curr == "€"

def test_extract_salary_parts_negotiable():
    s_from, s_to, curr = extract_salary_parts("Salary negotiable")
    assert s_from is None
    assert s_to is None
    assert curr is None
