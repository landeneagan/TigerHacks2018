import pymysql.cursors
# Environment variables are defined in app.yaml.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def SourceValidation(url):

    url.replace("https://","")
    url.replace("http://","")

    endIndex = url.index("/")
    endOfUrl = len(url) - 1
    url[:-(endOfUrl - endIndex)]

    httpUrl = 'http://' + url
    httpsUrl = 'https://' + url

    #connection = pymysql.connect(host='35.239.255.99', user='root', password='password', db='source_validation', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    #cursor = db.cursor()
    # db.Model.query.
    for score in db.Model.query(urls).filter(or_(url==httpsUrl, url==httpUrl)):
        print(score)
        send = score

    # with connection.cursor() as cursor:
    #     sql = "SELECT `score` FROM `urls` WHERE `url` = %s OR `url` = %s"
    #     cursor.execute(sql, (httpUrl, httpsUrl,))
    #     score = cursor.fetchone()
    #     print(score)
    # connection.close()

    return send

print(SourceValidation('https://www.cnet.com/news/google-plus-and-life-after-social-media-death/'))