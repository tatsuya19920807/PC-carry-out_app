#1ライブラリのインポート
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
#Flask: Pythonのマイクロウェブフレームワーク。
#render_template: HTMLテンプレートをレンダリングするための関数。
#request: リクエストデータを処理するためのオブジェクト。
#redirect: ユーザーを別のエンドポイントにリダイレクトするための関数。
#url_for: 指定されたエンドポイントのURLを生成するための関数。
#SQLAlchemy: データベース操作のためのORM（オブジェクトリレーショナルマッパー）。

#2アプリケーションの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#app = Flask(name): Flaskアプリケーションを初期化します。
#app.config[‘SQLALCHEMY_DATABASE_URI’]: SQLAlchemyのデータベースURIを設定します。
#app.config[‘SQLALCHEMY_TRACK_MODIFICATIONS’]: 変更追跡を無効にしてリソースを節約します。
#db = SQLAlchemy(app): FlaskアプリケーションにSQLAlchemyオブジェクトを初期化します。

# メール設定
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
mail = Mail(app)

#3データベースモデル
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)  # ここにcontentフィールドを追加

    def __repr__(self):
        return f'<Application {self.id} - {self.name}>'

#Application: データベーステーブルを表すクラス。
#name: 申請者の名前を格納する文字列型のカラム。
#email: 申請者のメールアドレスを格納する文字列型のカラム。
#reason: 申請理由を格納するテキスト型のカラム。
#repr: オブジェクトを文字列として表現するためのメソッド。

#4ルート
#インデックスルート
@app.route('/')
def index():
    return render_template('index.html')
#@app.route(‘/’): ホームページのルートを定義します。
#index(): index.htmlテンプレートをレンダリングする関数

#申請ルート
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        new_application = Application(name=name, email=email, content=content)

        try:
            db.session.add(new_application)
            db.session.commit()

            # メール送信
            msg = Message('新しい申請が提出されました',
                          sender='your-email@example.com',
                          recipients=['recipient@example.com'])
            msg.body = f"名前: {name}\nメール: {email}\n内容: {content}"
            mail.send(msg)

            return redirect(url_for('success'))
        except:
            return '申請の送信中に問題が発生しました'

    return render_template('submit.html')
#@app.route(‘/submit’, methods=[‘GET’, ‘POST’]): 申請を受け付けるルートを定義し、GETとPOSTメソッドの両方を許可します。
#submit(): フォームの送信を処理する関数。
#request.method == ‘POST’: リクエストメソッドがPOSTであるかを確認します。
#request.form: フォームデータにアクセスします。
#new_application: 新しいApplicationオブジェクトを作成します。
#db.session.add(new_application): 新しい申請をセッションに追加します。
#db.session.commit(): セッションをデータベースにコミットします。
#redirect(url_for(‘success’)): 送信が成功した場合、成功ページにリダイレクトします。
#render_template(‘submit.html’): リクエストメソッドがGETの場合、submit.htmlテンプレートをレンダリングします

#成功ルート                
@app.route('/success')
def success():
    return render_template('success.html')
#@app.route(‘/success’): 成功ページのルートを定義します。
#success(): success.htmlテンプレートをレンダリングする関数

#5アプリケーションの実行
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
#if name == “main”:: スクリプトが直接実行された場合のみ実行されるようにします。
#db.create_all(): データベーステーブルを作成します。
#app.run(debug=True): デバッグモードでFlaskアプリケーションを実行します