from fastapi import APIRouter

from template.replace_me.data import ReplaceMeManager, ReplaceMe

router = APIRouter(prefix="/replace_mes")


@router.get("")
async def replace_me_collection() -> dict[str, list[ReplaceMe]]:
    replace_mes: dict[str, ReplaceMe] = {}
    async for batch in ReplaceMeManager.get_all_primary_keys_batched():
        replace_mes.update(await ReplaceMeManager.get_items(batch))
    return {"items": [item for item in replace_mes.values()]}


@router.get("/{key}")
async def replace_me(key: str) -> ReplaceMe:
    replace_mes = await ReplaceMeManager.get_items([key])
    return replace_mes[key]
