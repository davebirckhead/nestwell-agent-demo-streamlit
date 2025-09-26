from typing import Dict, Any
from langgraph.graph import StateGraph, END

class State(dict):
    pass

def classify_intent(state: State) -> State:
    m = state['message'].lower()
    if any(k in m for k in ["lounge","recommend","bundle"]):
        state['intent'] = 'marketing'
    elif any(k in m for k in ["price","quote","units","by end of"]):
        state['intent'] = 'sales'
    elif any(k in m for k in ["order","delayed","cancel","return"]):
        state['intent'] = 'support'
    else:
        state['intent'] = 'kb'
    return state

def marketing_node(state: State, tools) -> State:
    items = tools['catalog'].recommend_bundle(state['message'])
    lead_id = tools['crm'].create_lead(state['user_id'], {"bundle": items})
    state['result'] = (f"Bundle rec: {', '.join([i['name'] for i in items])}. Created Lead {lead_id}. Schedule a call?",
                       ["high_intent_engagement","lead_created"])
    return state

def sales_node(state: State, tools) -> State:
    quote = tools['catalog'].price_quote(state['message'])
    evt = tools['crm'].create_opportunity(state['user_id'], quote)
    meeting = tools['calendar'].book_meeting(state['user_id'])
    state['result'] = (f"Quote ready: {quote['summary']}. Booked 30 min: {meeting['when']} ({meeting['link']}).",
                       ["opportunity_created","meeting_booked"])
    return state

def support_node(state: State, tools) -> State:
    status = tools['orders'].lookup(state['message'])
    if status.get('delayed'):
        credit = tools['helpdesk'].issue_goodwill(state['user_id'], 20)
        case = tools['helpdesk'].create_case(state['user_id'], f"Delay on {status['order_id']}", status)
        state['result'] = (f"Order {status['order_id']} delayed; expedited + ${credit['amount']} credit. Case {case['id']} opened.",
                           ["resolved_autonomously","goodwill_credit","case_with_context"])
    else:
        state['result'] = (f"Order {status.get('order_id','N/A')} on track. Anything else?", [])
    return state

def kb_node(state: State, tools) -> State:
    answer = tools['kb'].answer(state['message'])
    state['result'] = (answer, ["kb_response"])
    return state

def build_graph(tools):
    g = StateGraph(State)
    g.add_node("classify", classify_intent)
    g.add_node("marketing", lambda s: marketing_node(s, tools))
    g.add_node("sales", lambda s: sales_node(s, tools))
    g.add_node("support", lambda s: support_node(s, tools))
    g.add_node("kb", lambda s: kb_node(s, tools))
    g.set_entry_point("classify")
    g.add_conditional_edges("classify", lambda s: s['intent'], {
        "marketing":"marketing", "sales":"sales", "support":"support", "kb":"kb"
    })
    for n in ["marketing","sales","support","kb"]:
        g.add_edge(n, END)
    return g.compile()
