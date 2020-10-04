from requests.exceptions import ConnectionError
from unidecode import unidecode
from datetime import datetime
from parsel import Selector
from requests import get
from json import dump
from re import sub

XPATHS = {
    "papercount": "//span[@data-test='no-of-chapters']/text()",
    "papertitle": "//h1[@class='ChapterTitle']/text()",
    "authors": "//span[@class='authors-affiliations__name']/text()",
    "aff_indexes": "//ul[@class='authors-affiliations__indexes']/text()",
    "aff_institutes": "//span[@class='affiliation__name']/text()",
    "aff_cities": "//span[@class='affiliation__city']/text()",
    "aff_countries": "//span[@class='affiliation__country']/text()",
}

host = "https://link.springer.com/"
books = {
    # 2015: ["10.1007/978-3-319-24553-9"],
    # 2016: ["10.1007/978-3-319-46726-9", "10.1007/978-3-319-46720-7", "10.1007/978-3-319-46723-8"],
    # 2017: ["10.1007/978-3-319-66182-7", "10.1007/978-3-319-66185-8"],
    # 2018: ["10.1007/978-3-030-00928-1"],
    2019: ["10.1007/978-3-030-32239-7"],
}


def listdecode(strlist):
    return [sub("\n", "", unidecode(s)) for s in strlist]


data = {year: [] for year in books.keys()}
failed = {year: [] for year in books.keys()}
for year, codes in books.items():
    print(f"Year: {year}")
    for idx, code in enumerate(codes):
        book = f"{host}/book/{code}"
        try:
            selector = Selector(text=get(book).text)
            papers = int(sub("[^0-9]+", "", selector.xpath(XPATHS["papercount"]).get()))
            print(f"Book: {idx + 1}/{len(codes)}")
            print(f"Paper count: {papers}")

            # papers = 2  # DEBUG
            for i in range(papers):
                print(f"Paper: {i+1}/{papers}")
                paper = f"{host}/chapter/{code}_{i+1}"
                try:
                    selector = Selector(text=get(paper).text)
                    title = unidecode(selector.xpath(XPATHS["papertitle"]).get())
                    authors = listdecode(selector.xpath(XPATHS["authors"]).getall())
                    aff_indexes = listdecode(selector.xpath(XPATHS["aff_indexes"]).getall())
                    affiliations = {
                        "institutes": listdecode(selector.xpath(XPATHS["aff_institutes"]).getall()),
                        "cities": listdecode(selector.xpath(XPATHS["aff_cities"]).getall()),
                        "countries": listdecode(selector.xpath(XPATHS["aff_countries"]).getall()),
                    }
                    data[year].append(
                        {
                            "title": title,
                            "authors": authors,
                            "affiliations": affiliations,
                        }
                    )
                    print("Done.")

                # Write paper code to logs in case of connection failure
                except ConnectionError:
                    failed[year].append(paper)
                    print("Failed! Written to logs.")
            print("\n")

        # Write book code to logs in case of connection failure
        except ConnectionError:
            failed[year] = True
            print("Book failed! Written to logs.")


timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

with open(f"failure-{timestamp}.log", "w") as failure_log:
    dump(failed, failure_log)

with open(f"data-{timestamp}.json", "w") as data_json:
    dump(data, data_json)
