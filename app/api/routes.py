from fastapi import APIRouter
from app.controller.authController.auth_controller import router as auth_router
from app.controller.userController.user_controller import router as user_router
from app.controller.adressController.adress_controller import router as address_router
from app.controller.categoryController.category_controller import router as category_router
from app.controller.productController.product_controller import router as product_router
from app.controller.productImageController.product_image_controller import router as product_image_router
from app.controller.usercontroller.user_type_controller import router as user_type_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(address_router)
router.include_router(category_router)
router.include_router(product_router)
router.include_router(product_image_router)
router.include_router(user_type_router)
