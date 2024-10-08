import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class PromptCreator:
    @staticmethod
    def create_spam_prompt(feedback):
        chat_template = [
            SystemMessage(content="Meta Contexto\n## Você é um assistente encarregado de moderar feedbacks recebidos de usuários em um sistema online. Os feedbacks serão sempre relacionados ao uso de aplicativos na área de bem-estar e saúde mental.\nComo parte de suas responsabilidades, você deve identificar e filtrar mensagens de spam nos feedbacks.\n- Você tem uma ampla experiência em identificar padrões comuns em mensagens de spam.\n- Seu principal objetivo é manter a qualidade dos feedbacks ao remover mensagens de spam.\n- Você receberá um feedback e deve indicar se ele é considerado spam.\n\n## Cadeia de pensamento:\n#Quando receber um feedback, siga os seguintes procedimentos: \n1- Elenque em formato de tópicos todos os assuntos abordados no feedback.\n2- Analise se há pelo menos um desses tópicos que fuja completamente do contexto fornecido. Caso haja, isso significa que o feedback é um spam.\n\n## Formato da resposta: {\"topicos\": [<lista com todos os tópicos abordados no feedback>], \"spam\": \"<SIM ou NAO>\"}"),
            HumanMessage(content="Considere o seguinte feedback recebido:\n\n'''Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta'''\n\nAnalise o feedback e indique se ele é spam ou não. Retorne o json requerido no system."),
            AIMessage(content="{\"topicos\": [\"Usuário se mostra satisfeito com o uso do aplicativo\", \"Usuário sugere que seja possível realizar a edição do perfil\"], \"spam\": \"NAO\"}"),
            HumanMessage(content="Considere o seguinte feedback recebido:\n\n'''Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Assine já o seu plano acessando o site https://www.claro.com.br e garanta o primeiro mês grátis.'''\n\nAnalise o feedback e indique se ele é spam ou não. Retorne o json requerido no system."),
            AIMessage(content="{\"topicos\": [\"Usuário se mostra satisfeito com o uso do aplicativo\", \"Mensagem de venda de algum produto da Claro\"], \"spam\": \"SIM\"}"),
            HumanMessage(content=f"Considere o seguinte feedback recebido:\n\n{feedback}\n\nAnalise o feedback e indique se ele é spam ou não. Retorne o json requerido no system.")
        ]
        return chat_template
    
    @staticmethod
    def create_sentiment_analysis_prompt(feedback:str, codes:str):
        chat_template = [
            SystemMessage(content="Meta Contexto\n## Você é um assistente encarregado de analisar feedbacks recebidos de usuários em um sistema online. Os feedbacks serão sempre relacionados ao uso de aplicativos na área de bem-estar e saúde mental.\nComo parte de suas responsabilidades, você deve identificar se o feedback é positivo, negativo ou inconclusivo e se o usuário sugeriu alguma melhoria.\n\n## Cadeia de pensamento:\nQuando receber um feedback, siga os seguintes procedimentos:\n1- Elenque em formato de tópicos todos os assuntos abordados no feedback.\n2- Analise se o feedback é POSITIVO, NEGATIVO ou INCONCLUSIVO. ATENÇÃO: Feedbacks positivos podem incluir pontos de melhoria sugeridos pelo usuário.\n3- Elenque quais foram as melhorias sugeridas, caso haja alguma. Para cada melhoria, você deverá informar o código que a representa e uma descrição mais detalhada dessa melhoria. Você receberá uma lista de códigos já existentes, e caso a melhoria possa se encaixar em algum dos códigos fernecidos, utilize o mesmo. Caso contrário, crie um novo código que tenha um nome auto explicativo (exemplo: EDITAR_PERFIL, EDITAR_FORMA_DE_PAGAMENTO...).\n\n## Formato da resposta: {\"topicos\": [<lista com todos os tópicos abordados no feedback>], \"sentiment\": \"<POSITIVO, NEGATIVO ou INCONCLUSIVO>\", \"requested_features\": [{\"code\": \"<código que representa a melhoria proposta>\", \"reason\": \"<descrição da melhoria sugerida>\"}]}"),
            HumanMessage(content="Considere o seguinte feedback recebido:\n\n'''Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta'''\nConsidere também essa lista de código de melhorias: '''[EXCLUIR_CONTA, EDITAR_PERFIL]'''\nSiga a cadeia de pensamento proposta no system e retorne o json requerido."),
            AIMessage(content="{\"topicos\": [\"Usuário se mostra satisfeito com o uso do aplicativo\", \"Usuário sugere que seja possível realizar a edição do perfil\"], \"sentiment\": \"POSITIVO\", \"requested_features\": [{\"code\": \"EDITAR_PERFIL\", \"reason\": \"O usuário gostaria de realizar a edição do próprio perfil\"}]}"),
            HumanMessage(content=f"Considere o seguinte feedback recebido:\n\n{feedback}\n\nConsidere também essa lista de código de melhorias:\n\n{codes}\n\nSiga a cadeia de pensamento proposta no system e retorne o json requerido. ATENÇÃO: não retornar nada além do json. Você não precisa jsutificar a sua resposta.")
        ]
        return chat_template
    
    @staticmethod
    def create_email_prompt(feedback_percentages:str, requested_features:str):
        chat_template = [
            SystemMessage(content="Meta Contexto\n## Você é um assistente encarregado de escrever emails para stakeholders de uma empresa com informações relevantes de feedbacks dos usuários de uma plataforma online. Você receberá dados de porcentagens de feedbacks negativos e positivos e também quais foram as principais melhorias sugeridas pelos usuários.\nComo parte de suas responsabilidades, você deve escrever o e-mail referenciando-se diretamente aos stakeholders e incluindo as informações fornecidas. Além disso, indique por que é importante incluir cada uma das melhorias sugeridas pelos usuários.\n\n## Sobre o tom da resposta:\nSua linguagem deve ser formal, clara e objetiva."),
            HumanMessage(content=f"Considere as seguintes porcentagens de feedbacks recebidos:\n\n{feedback_percentages}\n\nConsidere também essa lista de melhorias sugeridas pelos usuários:\n\n{requested_features}\n\nCom base nessas informações, escreva o email requerido. Comece o email com 'Prezados,\n' e finalize com 'Atenciosamente,\nAlumind Bot.'")
        ]
        return chat_template