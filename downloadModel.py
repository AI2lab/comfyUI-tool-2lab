import argparse

from nodes.utils import  download_model

def main(node):
    print(f"Node: {node}")
    download_model(node)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="download models for custom node")

    # 添加一个可选参数 --node
    parser.add_argument('--node', type=str, default='', help='Specify the node folder name')

    # 解析命令行参数
    args = parser.parse_args()

    # 调用主函数并传递解析后的参数
    main(args.node)