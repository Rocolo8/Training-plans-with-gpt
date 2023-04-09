# backend/app/training_plan/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.training_plan import TrainingPlan
from app.database import get_db

router = APIRouter()


# devuelve el plan de entrenamiento para el ID de usuario especificado
@router.get('/{user_id}/training_plan')
def get_user_training_plan(user_id: int, db: Session = Depends(get_db)):
    training_plan = db.query(TrainingPlan).filter(TrainingPlan.user_id == user_id).all()
    if not training_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training plan not found")
    return training_plan


# crea un nuevo plan de entrenamiento con los datos proporcionados
@router.post('/{user_id}/training_plan')
def create_training_plan(user_id: int, plan_data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_training_plan = TrainingPlan(user_id=user_id, exercise=plan_data['exercise'], sets=plan_data['sets'],
                                     reps=plan_data['reps'], weight=plan_data.get('weight'))
    db.add(new_training_plan)
    db.commit()
    db.refresh(new_training_plan)

    return new_training_plan


# actualiza el plan de entrenamiento con los datos proporcionados.
@router.put('/{user_id}/training_plan/{plan_id}')
def update_training_plan(user_id: int, plan_id: int, plan_data: dict, db: Session = Depends(get_db)):
    training_plan = db.query(TrainingPlan).filter(TrainingPlan.user_id == user_id, TrainingPlan.id == plan_id).first()
    if not training_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training plan not found")

    for key, value in plan_data.items():
        if hasattr(training_plan, key):
            setattr(training_plan, key, value)

    db.commit()
    db.refresh(training_plan)
    return training_plan
