/* Copyright (C) 2003-2013 Runtime Revolution Ltd.
 
 This file is part of LiveCode.
 
 LiveCode is free software; you can redistribute it and/or modify it under
 the terms of the GNU General Public License v3 as published by the Free
 Software Foundation.
 
 LiveCode is distributed in the hope that it will be useful, but WITHOUT ANY
 WARRANTY; without even the implied warranty of MERCHANTABILITY or
 FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 for more details.
 
 You should have received a copy of the GNU General Public License
 along with LiveCode.  If not see <http://www.gnu.org/licenses/>.  */

#include <foundation.h>

#include "foundation-private.h"

////////////////////////////////////////////////////////////////////////////////

bool MCHandlerCreate(MCTypeInfoRef p_typeinfo, const MCHandlerCallbacks *p_callbacks, void *p_context, MCHandlerRef& r_handler)
{
    __MCHandler *self;
    if (!__MCValueCreate(kMCValueTypeCodeHandler, sizeof(__MCHandler) + p_callbacks -> size, (__MCValue*&)self))
        return false;
    
    MCMemoryCopy(self + 1, p_context, p_callbacks -> size);
    
    self -> typeinfo = MCValueRetain(p_typeinfo);
    self -> callbacks = p_callbacks;
    
    r_handler = self;
    
    return true;
}

bool MCHandlerInvoke(MCHandlerRef self, MCValueRef *p_arguments, uindex_t p_argument_count, MCValueRef& r_value)
{
    return self -> callbacks -> invoke(self + 1, p_arguments, p_argument_count, r_value);
}

////////////////////////////////////////////////////////////////////////////////

void __MCHandlerDestroy(__MCHandler *self)
{
    if (self -> callbacks -> release != nil)
        self -> callbacks -> release(self + 1);
}

hash_t __MCHandlerHash(__MCHandler *self)
{
    return MCHashPointer(self);
}

bool __MCHandlerIsEqualTo(__MCHandler *self, __MCHandler *other_self)
{
    return self == other_self;
}

bool __MCHandlerCopyDescription(__MCHandler *self, MCStringRef& r_desc)
{
    return false;
}

////////////////////////////////////////////////////////////////////////////////
