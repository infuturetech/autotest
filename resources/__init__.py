"边端智能盒子自动化测试仓"
import os


RESOURCE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))

test_algo_app_file = os.path.join(RESOURCE_DIR, "sample.tar.gz")


if __name__ == "__main__":
    print("边端智能盒子自动化测试仓")
    print(RESOURCE_DIR)
    print(test_algo_app_file)