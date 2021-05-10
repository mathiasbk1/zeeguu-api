import zeeguu_core
from zeeguu_core.sql.query_building import date_format

db = zeeguu_core.db


def exercise_correctness(user_id, cohort_id, start_date, end_date):

    # TODO: Use the cohort id in the query in order to ensure that we're only looking at the appropriate language

    query = """
        select o.outcome, count(o.outcome)
            from exercise as e
                join bookmark_exercise_mapping as bem
                    on bem.`exercise_id`=e.id
                join bookmark as b
                    on bem.bookmark_id=b.id
                join exercise_outcome as o
                    on e.outcome_id = o.id
            where b.user_id=:userid
                and	e.time > :startDate
                and	e.time < :endDate
            group by outcome
    """

    start_date_fmt = date_format(start_date)
    end_date_fmt = date_format(end_date)

    rows = db.session.execute(
        query, {"userid": user_id, "startDate": start_date_fmt, "endDate": end_date_fmt}
    )

    result = {}
    for row in rows:
        result[row[0]] = row[1]

    return result
