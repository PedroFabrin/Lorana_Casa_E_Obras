from fastapi import APIRouter
from app.controller.authController.auth_controller import router as auth_router
from app.controller.userController.user_controller import router as user_router
from app.controller.adressController.adress_controller import router as adress_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(adress_router)
