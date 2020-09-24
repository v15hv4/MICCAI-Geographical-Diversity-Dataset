from requests.exceptions import ConnectionError
from parsel import Selector
from requests import get
from json import dump
from re import sub

XPATHS = {
    "papercount": "//span[@data-test='no-of-chapters']/text()",
    "authors": "//span[@class='authors-affiliations__name']/text()",
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


def nfkd(strlist):
    return [sub("\xa0", " ", s) for s in strlist]


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

            for i in range(papers):
                paper = f"{host}/chapter/{code}_{i+1}"
                try:
                    selector = Selector(text=get(paper).text)
                    authors = nfkd(selector.xpath(XPATHS["authors"]).getall())
                    affiliations = {
                        "institutes": nfkd(selector.xpath(XPATHS["aff_institutes"]).getall()),
                        "cities": nfkd(selector.xpath(XPATHS["aff_cities"]).getall()),
                        "countries": nfkd(selector.xpath(XPATHS["aff_countries"]).getall()),
                    }
                    data[year].append(
                        {
                            "book": idx + 1,
                            "papers": papers,
                            "authors": authors,
                            "affiliations": affiliations,
                        }
                    )
                    print("Done.\n")
                except ConnectionError:
                    failed[year].append(paper)
                    print("Paper failed! Written to logs.")

        except ConnectionError:
            failed[year] = True
            print("Book failed! Written to logs.")

with open("failure.log", "w") as failure_log:
    dump(failed, failure_log)

with open("data.json", "w") as data_json:
    dump(data, data_json)
