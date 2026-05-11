import dataclasses
import httpx
from fastmcp import FastMCP
import argparse

from .load import load_http

# WB specs shared on github pages after WB blocked automatic downloads from https://dev.wildberries.ru
OPENAPI_DOWNLOAD_URI: str = "https://bigancientmammoth.github.io/wb-swagger/original"

@dataclasses.dataclass
class Scope:
    uri: str         # WB API uri
    spec_file: str   # Open API spec


SCOPES: dict[str, Scope] = {
    "general:user-management": Scope(uri="https://user-management-api.wildberries.ru", spec_file="01-general.yaml"),
    "general:common": Scope(uri="https://common-api.wildberries.ru", spec_file="01-general.yaml"),
    "general:feedbacks": Scope(uri="https://feedbacks-api.wildberries.ru", spec_file="01-general.yaml"),

    "products:discounts-prices": Scope(uri="https://discounts-prices-api.wildberries.ru", spec_file="02-products.yaml"),
    "products:content": Scope(uri="https://content-api.wildberries.ru", spec_file="02-products.yaml"),
    "products:marketplace": Scope(uri="https://marketplace-api.wildberries.ru", spec_file="02-products.yaml"),

    "orders-fbs": Scope(uri="https://marketplace-api.wildberries.ru", spec_file="03-orders-fbs.yaml"),
    "orders-dbw": Scope(uri="https://marketplace-api.wildberries.ru", spec_file="04-orders-dbw.yaml"),
    "orders-dbs": Scope(uri="https://marketplace-api.wildberries.ru", spec_file="05-orders-dbs.yaml"),
    "in-store-pickup": Scope(uri="https://marketplace-api.wildberries.ru", spec_file="06-in-store-pickup.yaml"),
    "orders-fbw": Scope(uri="https://supplies-api.wildberries.ru", spec_file="07-orders-fbw.yaml"),

    "promotion:dp-calendar": Scope(uri="https://dp-calendar-api.wildberries.ru", spec_file="08-promotion.yaml"),
    "promotion:advert-media": Scope(uri="https://advert-media-api.wildberries.ru", spec_file="08-promotion.yaml"),
    "promotion:advert": Scope(uri="https://advert-api.wildberries.ru", spec_file="08-promotion.yaml"),

    "communications:buyer-chat": Scope(uri="https://buyer-chat-api.wildberries.ru", spec_file="09-communications.yaml"),
    "communications:feedbacks": Scope(uri="https://feedbacks-api.wildberries.ru", spec_file="09-communications.yaml"),
    "communications:returns": Scope(uri="https://returns-api.wildberries.ru", spec_file="09-communications.yaml"),

    "tariffs": Scope(uri="https://common-api.wildberries.ru", spec_file="10-tariffs.yaml"),
    "analytics": Scope(uri="https://seller-analytics-api.wildberries.ru", spec_file="11-analytics.yaml"),

    "reports:seller-analytics": Scope(uri="https://seller-analytics-api.wildberries.ru", spec_file="12-reports.yaml"),
    "reports:statistics": Scope(uri="https://statistics-api.wildberries.ru", spec_file="12-reports.yaml"),

    "finances:statistics": Scope(uri="https://statistics-api.wildberries.ru", spec_file="13-finances.yaml"),
    "finances:finance": Scope(uri="https://finance-api.wildberries.ru", spec_file="13-finances.yaml"),
    "finances:documents": Scope(uri="https://documents-api.wildberries.ru", spec_file="13-finances.yaml"),
}


def main():
    parser = argparse.ArgumentParser(description="WB API")
    parser.add_argument("--token", required=True, help="API token")
    parser.add_argument("--scope", required=True, help="scope", choices=SCOPES.keys())
    parser.add_argument("--locale", required=False, help="locale (en, ru)", choices=("en", "ru"))
    args = parser.parse_args()

    locale: str = args.locale or "en"
    scope: Scope = SCOPES[args.scope]

    # load specs
    spec = load_http(f'{OPENAPI_DOWNLOAD_URI}/{locale}/{scope.spec_file}')

    # remove routes on other domains (iter over copy of keys)
    for path in list(spec["paths"].keys()):
        path_obj = spec["paths"][path]
        path_urls = [server["url"] for server in path_obj.get("servers", [])]
        is_matching = len(path_urls) == 0 or scope.uri in path_urls
        if not is_matching:
            del spec["paths"][path]

    client = httpx.AsyncClient(
        base_url=scope.uri,
        headers={"Authorization": "Bearer " + args.token},
    )
    mcp = FastMCP.from_openapi(
        openapi_spec=spec,
        client=client,
        name="WB API " + args.scope,
    )
    mcp.run()


if __name__ == "__main__":
    main()
