


create warehouse if not exists anime_analytics_wh 
    with warehouse_size='x-small'
    auto_suspend = 60 --suspend after 60 sec of inactivity
    auto_resume=TRUE --automatically resume from suspension at query execution
    initially_suspended=True; --start in suspended state to save cost
