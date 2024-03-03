from difflib import SequenceMatcher
import heapq


class QuestionMatcher:
    @staticmethod
    def match_question(user_input, questions, top_n=10):
        """
        使用模糊匹配算法查找与用户输入最相似的问答对的前top_n个问答对
        :param user_input: 用户输入的问题
        :param questions: 从数据库中获取的问答对列表，每个元素是一个字典包含'question'和'answer'字段
        :param top_n: 需要返回的最相似问答对的数量，默认为10
        :return: 匹配到的前top_n个最相似的问答对的列表，如果找不到匹配项，返回空列表
        """
        heap = []

        for q_dict in questions:
            question = q_dict.get('question', '')
            answer = q_dict.get('answer', '')
            document = q_dict.get('title', '')
            id = q_dict.get('id', '')
            ratio = QuestionMatcher.calculate_similarity(user_input, question)
            if len(heap) < top_n :
                # and ratio > 0.2
                heapq.heappush(heap, (ratio, question, answer, document, id))
            else:
                heapq.heappushpop(heap, (ratio, question, answer, document, id))

        best_matches = sorted(heap, reverse=True)
        return [{'question': match[1], 'answer': match[2], 'title': match[3], 'id':match[4]} for match in best_matches]

    @staticmethod
    def calculate_similarity(a, b):
        """
        计算两个字符串的相似度
        :param a: 字符串a
        :param b: 字符串b
        :return: 相似度比率，值范围为0到1
        """
        return SequenceMatcher(None, a, b).ratio()
