from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    month: Union[Unset, str] = UNSET,
    authorization: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    params: dict[str, Any] = {}

    params["month"] = month

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v0/usage.show",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    month: Union[Unset, str] = UNSET,
    authorization: Union[Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Show Usage

     List usage for the user.

    **Example**:
    ```
    GET <api_prefix>/usage.show?month=2024-12 HTTP/1.1
    Host: <zebrastream_host>
    Authorization: Bearer <management_api_key>
    ```

    Args:
        month (Union[Unset, str]): Month to show usage for, for instance 2024-12
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        month=month,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    month: Union[Unset, str] = UNSET,
    authorization: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Show Usage

     List usage for the user.

    **Example**:
    ```
    GET <api_prefix>/usage.show?month=2024-12 HTTP/1.1
    Host: <zebrastream_host>
    Authorization: Bearer <management_api_key>
    ```

    Args:
        month (Union[Unset, str]): Month to show usage for, for instance 2024-12
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        month=month,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    month: Union[Unset, str] = UNSET,
    authorization: Union[Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Show Usage

     List usage for the user.

    **Example**:
    ```
    GET <api_prefix>/usage.show?month=2024-12 HTTP/1.1
    Host: <zebrastream_host>
    Authorization: Bearer <management_api_key>
    ```

    Args:
        month (Union[Unset, str]): Month to show usage for, for instance 2024-12
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        month=month,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    month: Union[Unset, str] = UNSET,
    authorization: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Show Usage

     List usage for the user.

    **Example**:
    ```
    GET <api_prefix>/usage.show?month=2024-12 HTTP/1.1
    Host: <zebrastream_host>
    Authorization: Bearer <management_api_key>
    ```

    Args:
        month (Union[Unset, str]): Month to show usage for, for instance 2024-12
        authorization (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            month=month,
            authorization=authorization,
        )
    ).parsed
