import pygame
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///workload.db')
Base = declarative_base()
session = sessionmaker(bind=engine)
s = session()


class Results(Base):
    """Results database schema"""
    __tablename__ = 'Results'

    id = Column(Integer, primary_key=True)
    name = Column(String, default="Unknown")
    result = Column(Integer, default=0)


def remove_weakest(records):
    """Remove worst result"""
    results = [i.result for i in records]
    weakest = results.index(min(results))
    record_id = [i.id for i in records]
    x = s.query(Results).filter_by(id=record_id[weakest]).first()
    s.delete(x)
    s.commit()


def add(player_name, player_result):
    """Add new result to database"""
    s.add(Results(name=player_name, result=player_result))
    records = s.query(Results).all()
    if len(records) > 10:
        remove_weakest(records)
    s.commit()


def show_results(screen):
    """Display previous best results"""
    x = 100
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return 'menu'
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    label = []
    text = s.query(Results).order_by(Results.result.desc()).all()
    text = [i.name + ' ' + str(round(i.result, 3)) for i in text]
    for line in text:
        label.append(my_font.render(line, True, (0, 0, 0)))
    for i in label:
        screen.blit(i, (450, x))
        x += 60
    pygame.display.update()
    Base.metadata.create_all(engine)
    s.close()
    return None

