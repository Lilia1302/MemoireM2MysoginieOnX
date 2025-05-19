import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def get_tweet_text(tweet_id):
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)
        tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"
        driver.get(tweet_url)

        wait = WebDriverWait(driver, 10)

        try:
            tweet_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@data-testid="tweetText"]')
            ))
        except:
            try:
                tweet_element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@data-testid="cellInnerDiv"]//div[@lang]')
                ))
            except Exception as e:
                driver.quit()
                return f"[ERREUR XPATH] {str(e)}"

        tweet_text = tweet_element.text
        driver.quit()
        return tweet_text

    except Exception as e:
        return f"[ERREUR SELENIUM] {str(e)}"

# Charger les données
df_input = pd.read_csv(r"C:\Users\ULTRABOOK DELL\OneDrive - UPEC\Bureau\Mémoire M2\DataSets\BERT\MeTwo.csv", sep=";")

# Tester les 10 premiers seulement
results = []
for tweet_id in df_input["status_id"].head(10):
    print(f"🔍 Récupération du tweet {tweet_id}...")
    text = get_tweet_text(tweet_id)
    print(f"📄 Résultat : {text[:80]}{'...' if len(text) > 80 else ''}")
    results.append({"tweet_id": tweet_id, "tweet_text": text})
    time.sleep(3)

# Sauvegarder
df_output = pd.DataFrame(results)
df_output.to_csv("tweets_texts_test.csv", index=False, encoding="utf-8-sig")

print("✅ Test terminé ! Résultats dans tweets_texts_test.csv")
