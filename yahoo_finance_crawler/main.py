import argparse

from crawler import YahooFinanceCrawler

parser = argparse.ArgumentParser(description='Descrição do seu script.')
parser.add_argument(
    'region',
    type=str,
    help='O nome da região para ser usado como filtro de busca.'
)
args = parser.parse_args()

if __name__ == '__main__':
    try:
        region = args.region.lower()

        crawler = YahooFinanceCrawler(region)
        crawler.run()
    except KeyboardInterrupt:
        print('\nPrograma interrompido pelo usuário')
    except FileNotFoundError:
        print('Arquivo não encontrado')
    except Exception as e:
        print(e)
