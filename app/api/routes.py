from fastapi import APIRouter
from app.controller.authController.auth_controller import router as auth_router
from app.controller.userController.user_controller import router as user_router
from app.controller.adressController.adress_controller import router as adress_router
from app.controller.sectionController.section_controller import router as section_router
from app.controller.categoryController.category_controller import router as category_router
from app.controller.productController.product_controller import router as product_router
from app.controller.productImageController.product_image_controller import router as product_image_router
from app.controller.cartController.cart_controller import router as cart_router
from app.controller.orderController.order_controller import router as order_router
from app.controller.reportController.report_controller import router as report_router
from app.controller.dashboardController.dashboard_controller import router as dashboard_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(adress_router)
router.include_router(section_router)
router.include_router(category_router)
router.include_router(product_router)
router.include_router(product_image_router)
router.include_router(cart_router)
router.include_router(order_router)
router.include_router(report_router)
router.include_router(dashboard_router)
