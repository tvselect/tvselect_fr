import subprocess
import random
import getpass

cmd = "timedatectl | grep -i 'Time zone' | tr -s ' ' | cut -d ' ' -f4"
output = subprocess.Popen(
    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
)
stdout, stderr = output.communicate()
timezone = stdout.decode("utf-8")[:-1]

answers = ["oui", "non"]
answer = "maybe"

if timezone != "Europe/Paris":
    print(
        "Le fuseau horaire de votre box TV est {timezone}. Le fuseau horaire qui "
        "doit être configuré est 'Europe/Paris'. Si vous ne voulez pas changer de "
        "fuseau horaire, contactez-nous pour configurer votre box TV afin de "
        "pouvoir l'utiliser avec un fuseau horaire différent "
        "de 'Europe/Paris'.".format(timezone=timezone)
    )
    while answer.lower() not in answers:
        answer = input(
            "Voulez-vous changer le fuseau horaire pour 'Europe/Paris'?"
            " (répondre oui ou non): "
        )
    if answer.lower() == "oui":
        cmd = "sudo timedatectl set-timezone Europe/Paris"
        timezo = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        timezo.wait()
        print(
            "\nImportant: Veuillez rédemarrer la box TV puis relancer le programme install.py\n"
        )
        exit()
    else:
        exit()

cmd = "ls ~ | grep ^videos_select$"
output = subprocess.Popen(
    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
)
stdout, stderr = output.communicate()
ls_directory = stdout.decode("utf-8")[:-1]

if ls_directory == "":
    cmd = "mkdir ~/videos_select"
    directory = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    directory.wait()
    print("Le dossier videos_select a été créé dans votre dossier home.\n")

cmd = "sed -i '3s/.*/cd \/home\/'$USER'\/videos_select/' launch_record.sh"
sed = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
sed.wait()

print("Configuration des tâches cron du programme tv-select:\n")

cmd = 'curl -I https://tv-select.fr | grep HTTP | tail -1 | cut -d " " -f 2'
http = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stdout, stderr = http.communicate()
http_response = stdout.decode("ascii")[:-1]

if http_response != "200":
    print(
        "\nLa box tv-select n'est pas connectée à internet. Veuillez "
        "vérifier votre connection internet et relancer le programme "
        "d'installation.\n\n"
    )
    exit()

username = input(
    "Veuillez saisir votre identifiant de connexion (adresse "
    "email) sur tv-select.fr: "
)

password_tvrecord = getpass.getpass(
    "Veuillez saisir votre mot de passe sur " "tv-select.fr: "
)

cmd = "ls -a ~ | grep ^.netrc$"
output = subprocess.Popen(
    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
)
stdout, stderr = output.communicate()
ls_netrc = stdout.decode("utf-8")[:-1]

if ls_netrc == "":
    cmd = "touch ~/.netrc"
    touch = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    touch.wait()
    cmd = "chmod go= ~/.netrc"
    chmod = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

cmd = "echo $USER"
echo = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stdout, stderr = echo.communicate()
user = stdout.decode("utf-8")[:-1]

authprog_response = "403"

while authprog_response != "200":
    with open("/home/" + user + "/.netrc", "r") as file:
        lines = file.read().splitlines()

    try:
        position = lines.index("machine www.tv-select.fr")
        lines[position + 1] = "  login {username}".format(username=username)
        lines[position + 2] = "  password {password_tvrecord}".format(
            password_tvrecord=password_tvrecord
        )
    except ValueError:
        lines.append("machine www.tv-select.fr")
        lines.append("  login {username}".format(username=username))
        lines.append(
            "  password {password_tvrecord}".format(password_tvrecord=password_tvrecord)
        )

    with open("/home/" + user + "/.netrc", "w") as file:
        for line in lines:
            file.write(line + "\n")

    cmd = 'curl -iSn https://www.tv-select.fr/api/v1/prog | grep HTTP | cut -d " " -f 2'
    authprog = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = authprog.communicate()
    authprog_response = stdout.decode("ascii")[:-1]

    if authprog_response != "200":
        try_again = input(
            "Le couple identifiant de connexion et mot de passe "
            "est incorrecte\nVoulez-vous essayer de nouveau?(oui ou non): "
        )
        answer_hide = "maybe"
        if try_again.lower() == "oui":
            username = input(
                "Veuillez saisir de nouveau votre identifiant de connexion (adresse email) sur TV-select.fr: "
            )
            while answer_hide.lower() not in answers:
                answer_hide = input(
                    "Voulez-vous afficher le mot de passe que vous saisissez "
                    "pour que cela soit plus facile? (répondre par oui ou non): "
                )
            if answer_hide.lower() == "oui":
                password_tvrecord = input(
                    "Veuillez saisir de nouveau votre mot de passe sur TV-select.fr: "
                )
            else:
                password_tvrecord = getpass.getpass(
                    "Veuillez saisir de nouveau votre mot de passe sur TV-select.fr: "
                )
        else:
            exit()

heure = random.randint(6, 23)
minute = random.randint(0, 58)
minute_2 = minute + 1

answers = ["oui", "non"]

if heure < 10:
    heure_print = "0" + str(heure)
else:
    heure_print = str(heure)

if minute < 10:
    minute_print = "0" + str(minute)
else:
    minute_print = str(minute)

answer = input(
    "\nVotre box TV-select va être configuré pour demander "
    "les informations nécessaires aux enregistrements à "
    "{heure}:{minute} . Votre box TV-select n'a besoin d'être "
    "connectée à internet seulement pendant 1 seconde par jour "
    "pour obtenir les informations nécessaires. Si votre box "
    "TV-select ne peut pas être connecté à internet à l'heure proposée, "
    "vous pouvez définir l'horaire manuellement. Voulez-vous changer "
    "l'horaire de téléchargement de vos informations personnalisées "
    "d'enregistrements? Répondez par oui si vous voulez changer l'horaire "
    "de {heure}H{minute} ou non si votre connection internet sera "
    "disponible à cette horaire: \n".format(heure=heure_print, minute=minute_print)
)

while answer.lower() not in answers:
    answer = input("Veuillez répondre par oui ou non: ")

if answer.lower() == "oui":
    heure = 24
    while heure < 6 or heure > 23:
        heure = int(
            input(
                "Choisissez une heure entre 6 et 23 (si vous ne "
                "pouvez avoir une connection internet que entre minuit "
                "et 6 heures du matin, contactez le support de "
                "TV-select afin de contourner cette restriction): "
            )
        )
    minute = 60
    while minute < 0 or minute > 58:
        minute = int(input("Choisissez les minutes entre 0 et 58: "))

    if heure < 10:
        heure_print = "0" + str(heure)
    else:
        heure_print = str(heure)

    if minute < 10:
        minute_print = "0" + str(minute)
    else:
        minute_print = str(minute)

    print(
        "\nVotre box TV-select va être configuré pour demander les "
        "informations nécessaires aux enregistrements à "
        "{heure}H{minute}".format(heure=heure_print, minute=minute_print)
    )
    minute_2 = minute + 1

cmd = "crontab -l > cron_tasks.sh"
crontab_init = subprocess.Popen(
    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
)
crontab_init.wait()

with open("cron_tasks.sh", "r") as crontab_file:
    cron_lines = crontab_file.readlines()

curl = (
    "{minute} {heure} * * * export USER='{user}' && "
    "curl -H 'Accept: application/json;"
    "indent=4' -n "
    "https://www.tv-select.fr/api/v1/prog > /home/$USER/box/info_"
    "progs.json 2>> /var/tmp/cron_curl.log\n".format(
        user=user,
        minute=minute,
        heure=heure,
    )
)

cron_launch = (
    "{minute_2} {heure} * * * export USER='{user}' && "
    "cd /home/$USER/box && "
    "bash cron_launch_record.sh\n".format(user=user, minute_2=minute_2, heure=heure)
)

cron_lines = [curl if "www.tv-select.fr" in cron else cron for cron in cron_lines]
cron_lines = [cron_launch if "/box &&" in cron else cron for cron in cron_lines]

cron_lines_join = "".join(cron_lines)

if "www.tv-select.fr" not in cron_lines_join:
    cron_lines.append(curl)
if "cd /home/$USER/box &&" not in cron_lines_join:
    cron_lines.append(cron_launch)

with open("cron_tasks.sh", "w") as crontab_file:
    for cron_task in cron_lines:
        crontab_file.write(cron_task)

cmd = "crontab cron_tasks.sh"
cron = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
cron.wait()
cmd = "rm cron_tasks.sh"
rm = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

print("\nLes tâches cron de votre box TV-select sont maintenant configurés!\n")
