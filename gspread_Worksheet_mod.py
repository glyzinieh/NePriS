import gspread

def get_all_dicts(self) -> list[dict]:
    dicts_data = []
    lists_data = self.get_all_values()
    header = lists_data[0]
    body = lists_data[1:]
    for i in body:
        dicts_data.append(dict(zip(header, i)))
    return dicts_data

setattr(gspread.Worksheet,'get_all_dicts',get_all_dicts)
