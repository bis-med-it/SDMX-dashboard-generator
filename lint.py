from pylint import lint
import os
import anybadge

run = lint.Run(["src"], do_exit=False)
score = run.linter.stats.global_note

with open("codequality_reports/pylint_report.txt", "w", encoding="utf8") as my_file:
    my_file.write("Your code has been rated at {}/10".format(score))



# Define thresholds: <2=red, <4=orange <8=yellow <10=green
thresholds = {2: 'red',
              4: 'orange',
              6: 'yellow',
              8: 'green'}

badge = anybadge.Badge('pylint', round(score, 2), thresholds=thresholds)
badge_path = r'images\\pylint.svg'
if os.path.exists(badge_path):
    os.remove(badge_path)
badge.write_badge(badge_path)