@app.cli.command("seed_countries")
def seed_countries():
    country1 = Country(
        id=1, 
        name="Afghanistan", 
        lgbt_legal_protections=False, 
        population=39835428, 
        gdp=20861234993, 
        hdi=0.511, 
        safety_rating=None, 
        tourism_rating=None, 
        overal_rating=None)
    db.session.add(country1)
    country2 = Country(
        id=2, 
        name="Albania", 
        lgbt_legal_protections=False, 
        population=2845955, 
        gdp=15700000000, 
        hdi=0.795, 
        safety_rating=None, 
        tourism_rating=None, 
        overal_rating=None)
    db.session.add(country2)

    country3 = Country(
            id=3, 
            name="Algeria", 
            lgbt_legal_protections=False, 
            population=44616626, 
            gdp=162800000000, 
            hdi=0.759, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country3)

    country4 = Country(
            id=4, 
            name="Andorra", 
            lgbt_legal_protections=False, 
            population=77354, 
            gdp=2900000000, 
            hdi=0.868, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country4)

    country5 = Country(
            id=5, 
            name="Angola", 
            lgbt_legal_protections=False, 
            population=32866272, 
            gdp=85300000000, 
            hdi=0.581, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country5)

    country6 = Country(
            id=6, 
            name="Antigua and Barbuda", 
            lgbt_legal_protections=False, 
            population=103050, 
            gdp=1700000000, 
            hdi=0.778, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country6)

    country7 = Country(
            id=7, 
            name="Argentina", 
            lgbt_legal_protections=False, 
            population=45267449, 
            gdp=383800000000, 
            hdi=0.830, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country7)

    country8 = Country(
            id=8, 
            name="Armenia", 
            lgbt_legal_protections=False, 
            population=2963234, 
            gdp=14700000000, 
            hdi=0.776, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country8)

    country9 = Country(
            id=9, 
            name="Australia", 
            lgbt_legal_protections=False, 
            population=25687041, 
            gdp=1400000000000, 
            hdi=0.944, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country9)

    country10 = Country(
            id=10, 
            name="Austria", 
            lgbt_legal_protections=False, 
            population=8917205, 
            gdp=487500000000, 
            hdi=0.922, 
            safety_rating=None, 
            tourism_rating=None, 
            overal_rating=None)
    db.session.add(country10)

    country11 = Country(
            id=11,
            name="Azerbaijan",
            lgbt_legal_protections=False,
            population=10067108,
            gdp=47500000000,
            hdi=0.756,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
    db.session.add(country11)

            country12 = Country(
            id=12,
            name="Bahamas",
            lgbt_legal_protections=False,
            population=393248,
            gdp=13700000000,
            hdi=0.807,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
    db.session.add(country12)

            country13 = Country(
            id=13,
            name="Bahrain",
            lgbt_legal_protections=False,
            population=1569439,
            gdp=36300000000,
            hdi=0.852,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
    db.session.add(country13)

            country14 = Country(
            id=14,
            name="Bangladesh",
            lgbt_legal_protections=False,
            population=169872845,
            gdp=352200000000,
            hdi=0.632,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
            db.session.add(country14)

            country15 = Country(
            id=15,
            name="Barbados",
            lgbt_legal_protections=False,
            population=287711,
            gdp=5000000000,
            hdi=0.813,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
            db.session.add(country15)

            country16 = Country(
            id=16,
            name="Belarus",
            lgbt_legal_protections=False,
            population=9466856,
            gdp=60200000000,
            hdi=0.817,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
            db.session.add(country16)

            country17 = Country(
            id=17,
            name="Belgium",
            lgbt_legal_protections=False,
            population=11632357,
            gdp=528300000000,
            hdi=0.931,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
            db.session.add(country17)

            country18 = Country(
            id=18,
            name="Belize",
            lgbt_legal_protections=False,
            population=397628,
            gdp=1800000000,
            hdi=0.716,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
            db.session.add(country18)

            country19 = Country(
            id=19,
            name="Benin",
            lgbt_legal_protections=False,
            population=12301739,
            gdp=14400000000,
            hdi=0.545,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
            db.session.add(country19)

            country20 = Country(
            id=20,
            name="Bhutan",
            lgbt_legal_protections=False,
            population=771612,
            gdp=3000000000,
            hdi=0.654,
            safety_rating=None,
            tourism_rating=None,
            overall_rating=None)
            db.session.add(country20)

        db.session.commit()
        print("Table seeded!")