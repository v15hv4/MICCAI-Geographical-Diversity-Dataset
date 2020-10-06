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
    "aff_indexes": "(//ul[@class='authors-affiliations__indexes u-inline-list'])",
    "aff_institutes": "//span[@class='affiliation__name']/text()",
    "aff_cities": "//span[@class='affiliation__city']/text()",
    "aff_countries": "//span[@class='affiliation__country']/text()",
}

host = "https://link.springer.com/"
books = {
    1998: ["10.1007/BFb0056181"],
    1999: ["10.1007/10704282"],
    2000: ["10.1007/b12345"],
    2001: ["10.1007/3-540-45468-3"],
    2002: ["10.1007/3-540-45786-0", "10.1007/3-540-45787-9"],
    2003: ["10.1007/b93810", "10.1007/b93811"],
    2004: ["10.1007/b100265", "10.1007/b100270"],
    2005: ["10.1007/11566465", "10.1007/11566489"],
    2006: ["10.1007/11866565", "10.1007/11866763"],
    2007: ["10.1007/978-3-540-75757-3", "10.1007/978-3-540-75759-7"],
    2008: ["10.1007/978-3-540-85988-8", "10.1007/978-3-540-85990-1"],
    2009: ["10.1007/978-3-642-04268-3", "10.1007/978-3-642-04271-3"],
    2010: ["10.1007/978-3-642-15705-9", "10.1007/978-3-642-15745-5", "10.1007/978-3-642-15711-0"],
    2011: ["10.1007/978-3-642-23623-5", "10.1007/978-3-642-23629-7", "10.1007/978-3-642-23626-6"],
    2012: ["10.1007/978-3-642-33415-3", "10.1007/978-3-642-33418-4", "10.1007/978-3-642-33454-2"],
    2013: ["10.1007/978-3-642-40811-3", "10.1007/978-3-642-40763-5", "10.1007/978-3-642-40760-4"],
    2014: ["10.1007/978-3-319-10404-1", "10.1007/978-3-319-10470-6", "10.1007/978-3-319-10443-0"],
    2015: ["10.1007/978-3-319-24553-9", "10.1007/978-3-319-24571-3", "10.1007/978-3-319-24574-4"],
    2016: ["10.1007/978-3-319-46726-9", "10.1007/978-3-319-46720-7", "10.1007/978-3-319-46723-8"],
    2017: ["10.1007/978-3-319-66182-7", "10.1007/978-3-319-66185-8", "10.1007/978-3-319-66179-7"],
    2018: ["10.1007/978-3-030-00928-1", "10.1007/978-3-030-00934-2", "10.1007/978-3-030-00931-1", "10.1007/978-3-030-00937-3"],
    2019: ["10.1007/978-3-030-32239-7", "10.1007/978-3-030-32245-8", "10.1007/978-3-030-32248-9", "10.1007/978-3-030-32251-9", "10.1007/978-3-030-32254-0", "10.1007/978-3-030-32226-7"],
    2020: ["10.1007/978-3-030-59710-8", "10.1007/978-3-030-59713-9", "10.1007/978-3-030-59716-0", "10.1007/978-3-030-59719-1", "10.1007/978-3-030-59722-1", "10.1007/978-3-030-59725-2", "10.1007/978-3-030-59728-3"],
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

            # papers = 2  
            for i in range(papers):
                print(f"Paper: {i+1}/{papers}")
                paper = f"{host}/chapter/{code}_{i+1}"
                try:
                    selector = Selector(text=get(paper).text)
                    title = unidecode(selector.xpath(XPATHS["papertitle"]).get())
                    authors = listdecode(selector.xpath(XPATHS["authors"]).getall())
                    aff_indexes = []
                    for index, _ in enumerate(authors):
                        try:
                            aff_index = (listdecode(Selector(selector.xpath(XPATHS["aff_indexes"] + "[" + str(index + 1) + "]").get()).xpath('//li/text()').getall()))
                            aff_indexes.append(aff_index)
                        except:
                            pass
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
                            "affiliations_index": aff_indexes,
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

with open(f"data/failure-{timestamp}.log", "w") as failure_log:
    dump(failed, failure_log)

with open(f"data/data-{timestamp}.json", "w") as data_json:
    dump(data, data_json, indent=4, separators=(',', ': '))
